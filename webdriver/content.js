const CDP = require('chrome-remote-interface');
const fs = require('fs');

// global settings
const filename = 'headless-results.png';
const url = 'https://intoli.com/blog/making-chrome-headless-undetectable/chrome-headless-test.html';
const userAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

CDP(async function(client) {
  const {Network, Page, Security} = client;
  await Page.enable();
  await Network.enable();
  await Network.setUserAgentOverride({userAgent});

  // ignore all certificate errors to support mitmproxy certificates
  await Security.enable();
  await Security.setOverrideCertificateErrors({override: true});
  Security.certificateError(({eventId}) => {
    Security.handleCertificateError({
        eventId,
        action: 'continue'
    });
  });

  setTimeout(async function() {
    // save the screenshot
    const screenshot = await Page.captureScreenshot({format: 'png'});
    const buffer = new Buffer(screenshot.data, 'base64');
    fs.writeFile(filename, buffer, 'base64', function(err) {
      if (err) {
        console.error(`Error saving screenshot: ${err}`);
      } else {
        console.log(`"${filename}" written successfully.`);
      }
      client.close();
    });
  }, 1000); // 1 second delay for the tests to complete
}).on('error', err => {
  console.error(`Error connecting to Chrome: ${err}`);
});

    // Overwrite the `languages` property to use a custom getter.
  Object.defineProperty(navigator, 'languages', {
    get: function() {
      return ['en-US', 'en'];
    },
  });


  //
  // Bypass the Plugins Test.
  //

  // Overwrite the `plugins` property to use a custom getter.
  Object.defineProperty(navigator, 'plugins', {
    get: function() {
      // This just needs to have `length > 0`, but we could mock the plugins too.
      return [1, 2, 3, 4, 5];
    },
  });

  //
  // Bypass the WebGL test.
  //

  const getParameter = WebGLRenderingContext.getParameter;
  WebGLRenderingContext.prototype.getParameter = function(parameter) {
    // UNMASKED_VENDOR_WEBGL
    if (parameter === 37445) {
      return 'Google Inc.';
    }
    // UNMASKED_RENDERER_WEBGL
    if (parameter === 37446) {
      return 'ANGLE (NVIDIA Corporation, GeForce GTX 1050 Ti/PCIe/SSE2, OpenGL 4.5 core)';
    }

    return getParameter(parameter);
  };

  //
  // Bypass the Broken Image Test.
  //

  ['height', 'width'].forEach(property => {
    // Store the existing descriptor.
    const imageDescriptor = Object.getOwnPropertyDescriptor(HTMLImageElement.prototype, property);

    // Redefine the property with a patched descriptor.
    Object.defineProperty(HTMLImageElement.prototype, property, {
      ...imageDescriptor,
      get: function() {
        // Return an arbitrary non-zero dimension if the image failed to load.
        if (this.complete && this.naturalHeight == 0) {
          return 20;
        }
        // Otherwise, return the actual dimension.
        return imageDescriptor.get.apply(this);
      },
    });
  });

  //
  // Bypass the Retina/HiDPI Hairline Feature Test.
  //

  // Store the existing descriptor.
  const elementDescriptor = Object.getOwnPropertyDescriptor(HTMLElement.prototype, 'offsetHeight');

  // Redefine the property with a patched descriptor.
  Object.defineProperty(HTMLDivElement.prototype, 'offsetHeight', {
    ...elementDescriptor,
    get: function() {
      if (this.id === 'modernizr') {
          return 1;
      }
      return elementDescriptor.get.apply(this);
    },
  });