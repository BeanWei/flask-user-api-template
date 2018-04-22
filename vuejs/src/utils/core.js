/**
 * JS-MD5加密用户密码
 * @param  pwd
 */
export const encryptedPassword =(pwd) => {
    let md5 = require('js-md5');
    let pwdkey = md5(pwd);
    return pwdkey;
  }
  