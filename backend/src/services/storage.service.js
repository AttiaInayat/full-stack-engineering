import ImageKit from '@imagekit/nodejs';
require("dotenv").config();

const client = new ImageKit({
  privateKey: process.env['IMAGEKIT_PRIVATE_KEY'],
});
