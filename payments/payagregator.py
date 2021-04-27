from project_shared import debug
from .fkagregator import FreeKassaAgregator


class PaymentAgregator():
    payment_agregator = None
    last_error = ""

    def creator(self, agregator: str):
        if agregator == 'Free Kassa':
            debug("Try create Free Kassa payment method")
            self.payment_agregator = FreeKassaAgregator()

    def clear(self):
        del self.payment_agregator

    def get_status(self):
        if self.payment_agregator is None:
            self.last_error = "Can not get Status -> Payment Agregator not created"
            return 'error'
        else:
            return self.payment_agregator.get_status()

    def to_pay(self):
        pass

    def get_last_error(self):
        if self.payment_agregator is None:
            return "Can not get Status -> Payment Agregator not created"
        else:
            return self.payment_agregator.get_last_error()

    def get_payment_link(self, order_id, summ, email='', description='') -> str:
        debug("PaymentAgregator: get_payment_link")
        if self.payment_agregator is None:
            return "Can not get Status -> Payment Agregator not created"
        else:
            return self.payment_agregator.get_payment_link(order_id, summ, email, description)
