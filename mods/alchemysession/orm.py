from typing import Optional, Tuple, Any, Union, TYPE_CHECKING
import datetime

from sqlalchemy import orm

from telethon.sessions.memory import MemorySession, _SentFileType
from telethon import utils
from telethon.crypto import AuthKey
from telethon.tl.types import (
    InputPhoto, InputDocument, PeerUser, PeerChat, PeerChannel, updates,
    InputPeerUser, InputPeerChat, InputPeerChannel
)
from telethon.tl import TLObject

if TYPE_CHECKING:
    from .sqlalchemy import AlchemySessionContainer


class AlchemySession(MemorySession):
    def __init__(self, container: 'AlchemySessionContainer', session_id: str) -> None:
        super().__init__()
        self.container = container
        self.db = container.db
        self.engine = container.db_engine
        self.Version, self.Session, self.Entity, self.SentFile, self.UpdateState = (
            container.Version, container.Session, container.Entity,
            container.SentFile, container.UpdateState)
        self.session_id = session_id
        self._load_session()

    def _load_session(self) -> None:
        sessions = self._db_query(self.Session).all()
        session = sessions[0] if sessions else None
        if session:
            self._dc_id = session.dc_id
            self._server_address = session.server_address
            self._port = session.port
            self._auth_key = AuthKey(data=session.auth_key)

    def clone(self, to_instance=None) -> MemorySession:
        return super().clone(MemorySession())

    def _get_auth_key(self) -> Optional[AuthKey]:
        sessions = self._db_query(self.Session).all()
        session = sessions[0] if sessions else None
        if session and session.auth_key:
            return AuthKey(data=session.auth_key)
        return None

    def set_dc(self, dc_id: str, server_address: str, port: int) -> None:
        super().set_dc(dc_id, server_address, port)
        self._update_session_table()
        self._auth_key = self._get_auth_key()

    def get_update_state(self, entity_id: int) -> Optional[updates.State]:
        row = self.UpdateState.query.get((self.session_id, entity_id))
        if row:
            date = datetime.datetime.utcfromtimestamp(row.date)
            return updates.State(row.pts, row.qts, date, row.seq, row.unread_count)
        return None

    def set_update_state(self, entity_id: int, row: Any) -> None:
        if row:
            self.db.merge(self.UpdateState(session_id=self.session_id, entity_id=entity_id,
                                           pts=row.pts, qts=row.qts, date=row.date.timestamp(),
                                           seq=row.seq,
                                           unread_count=row.unread_count))
            self.save()

    @MemorySession.auth_key.setter
    def auth_key(self, value: AuthKey) -> None:
        self._auth_key = value
        self._update_session_table()

    def _update_session_table(self) -> None:
        self.Session.query.filter(self.Session.session_id == self.session_id).delete()
        self.db.add(self.Session(session_id=self.session_id, dc_id=self._dc_id,
                                 server_address=self._server_address, port=self._port,
                                 auth_key=(self._auth_key.key if self._auth_key else b'')))

    def _db_query(self, dbclass: Any, *args: Any) -> orm.Query:
        return dbclass.query.filter(
            dbclass.session_id == self.session_id, *args
        )

    def save(self) -> None:
        self.container.save()

    def close(self) -> None:
        # Nothing to do here, connection is managed by AlchemySessionContainer.
        pass

    def delete(self) -> None:
        self._db_query(self.Session).delete()
        self._db_query(self.Entity).delete()
        self._db_query(self.SentFile).delete()
        self._db_query(self.UpdateState).delete()

    def _entity_values_to_row(self, id: int, hash: int, username: str, phone: str, name: str,
                              user_status: str, profile_lang: str, balance: float, referral: int,
                              subscribe_level: enumerate, expired: str, reserved_1: int,
                              reserved_2: str
                              ) -> Any:
        return self.Entity(session_id=self.session_id, id=id, hash=hash,
                           username=username, phone=phone, name=name,
                           user_status=user_status, profile_lang=profile_lang, balance=balance,
                           referral=referral, subscribe_level=subscribe_level, expired=expired,
                           reserved_1=reserved_1, reserved_2=reserved_2
        )#TODO ADD FIELDS

    def _entities_to_rows(self, tlo):
        if not isinstance(tlo, TLObject) and utils.is_list_like(tlo):
            # This may be a list of users already for instance
            entities = tlo
        else:
            entities = []
            if hasattr(tlo, 'user'):
                entities.append(tlo.user)
            if hasattr(tlo, 'chats') and utils.is_list_like(tlo.chats):
                entities.extend(tlo.chats)
            if hasattr(tlo, 'users') and utils.is_list_like(tlo.users):
                entities.extend(tlo.users)

        rows = []  # Rows to add (id, hash, username, phone, name)
        for e in entities:
            row = self._entity_to_row(e)
            if row:
                rows.append(row)
        return rows

    def _entity_to_row(self, e):
        if not isinstance(e, TLObject):
            return
        try:
            p = utils.get_input_peer(e, allow_self=False)
            marked_id = utils.get_peer_id(p)
        except TypeError:
            # Note: `get_input_peer` already checks for non-zero `access_hash`.
            #        See issues #354 and #392. It also checks that the entity
            #        is not `min`, because its `access_hash` cannot be used
            #        anywhere (since layer 102, there are two access hashes).
            return

        if isinstance(p, (InputPeerUser, InputPeerChannel)):
            p_hash = p.access_hash
        elif isinstance(p, InputPeerChat):
            p_hash = 0
        else:
            return

        username = getattr(e, 'username', None) or None
        if username is not None:
            username = username.lower()
        phone = getattr(e, 'phone', None)
        name = utils.get_display_name(e) or None
        user_status = str(getattr(e, 'status', None))
        profile_lang = getattr(e, 'lang_code', None)

        ext_rows = self.get_entity_ext_rows_by_id(marked_id)
        balance = ext_rows[0] if ext_rows else  0
        referral = ext_rows[1] if ext_rows else  0
        subscribe_level = ext_rows[2] if ext_rows else 'Free'
        expired = ext_rows[3] if ext_rows else None
        reserved_1 = ext_rows[4] if ext_rows else None
        reserved_2 = ext_rows[5] if ext_rows else None
        return self._entity_values_to_row(
            marked_id, p_hash, username, phone, name, user_status, profile_lang, balance, referral,
            subscribe_level, expired, reserved_1, reserved_2
        )

    def process_entities(self, tlo: Any) -> None:
        rows = self._entities_to_rows(tlo)
        if not rows:
            return

        for row in rows:
            self.db.merge(row)
        self.save()

    def get_entity_rows_by_phone(self, key: str) -> Optional[Tuple[int, int]]:
        row = self._db_query(self.Entity,
                             self.Entity.phone == key).one_or_none()
        return (row.id, row.hash) if row else None

    def get_entity_rows_by_username(self, key: str) -> Optional[Tuple[int, int]]:
        row = self._db_query(self.Entity,
                             self.Entity.username == key).one_or_none()
        return (row.id, row.hash) if row else None

    def get_entity_rows_by_name(self, key: str) -> Optional[Tuple[int, int]]:
        row = self._db_query(self.Entity,
                             self.Entity.name == key).one_or_none()
        return (row.id, row.hash) if row else None

    def get_entity_rows_by_id(self, key: int, exact: bool = True) -> Optional[Tuple[int, int]]:
        if exact:
            query = self._db_query(self.Entity, self.Entity.id == key)
        else:
            ids = (
                utils.get_peer_id(PeerUser(key)),
                utils.get_peer_id(PeerChat(key)),
                utils.get_peer_id(PeerChannel(key))
            )
            query = self._db_query(self.Entity, self.Entity.id.in_(ids))

        row = query.one_or_none()
        return (row.id, row.hash) if row else None

    def get_entity_ext_rows_by_id(self, key: int, exact: bool = True) -> Optional[Tuple[int, int]]:
        if exact:
            query = self._db_query(self.Entity, self.Entity.id == key)
        else:
            ids = (
                utils.get_peer_id(PeerUser(key)),
                utils.get_peer_id(PeerChat(key)),
                utils.get_peer_id(PeerChannel(key))
            )
            query = self._db_query(self.Entity, self.Entity.id.in_(ids))

        row = query.one_or_none()
        return (row.balance, row.referral, row.subscribe_level,
                row.expired, row.reserved_1, row.reserved_2
                ) if row else None

    def get_file(self, md5_digest: str, file_size: int, cls: Any) -> Optional[Tuple[int, int]]:
        row = self._db_query(self.SentFile,
                             self.SentFile.md5_digest == md5_digest,
                             self.SentFile.file_size == file_size,
                             self.SentFile.type == _SentFileType.from_type(
                                 cls).value).one_or_none()
        return (row.id, row.hash) if row else None

    def cache_file(self, md5_digest: str, file_size: int,
                   instance: Union[InputDocument, InputPhoto]) -> None:
        if not isinstance(instance, (InputDocument, InputPhoto)):
            raise TypeError("Cannot cache {} instance".format(type(instance)))

        self.db.merge(
            self.SentFile(session_id=self.session_id, md5_digest=md5_digest, file_size=file_size,
                          type=_SentFileType.from_type(type(instance)).value,
                          id=instance.id, hash=instance.access_hash))
        self.save()
