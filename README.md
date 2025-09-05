<p align="center">
  <a href="https://github.com/gospider007/fingerproxy"><img src="https://go.dev/images/favicon-gopher.png"></a>
</p>
<p align="center">A crawler-focused forward proxy with fingerprint spoofing</p>
<p align="center">
<a href="https://github.com/gospider007/fingerproxy">
    <img src="https://img.shields.io/github/last-commit/gospider007/fingerproxy">
</a>
<a href="https://github.com/gospider007/fingerproxy">
    <img src="https://img.shields.io/badge/build-passing-brightgreen">
</a>
<a href="https://github.com/gospider007/fingerproxy">
    <img src="https://img.shields.io/badge/language-golang-brightgreen">
</a>
</p>

---

<h2 align="center">Fingerproxy is a fully featured Golang-based forward proxy app with browser fingerprint spoofing. With just a few lines of code, you can enable powerful fingerprint proxy capabilities. It provides unified support for HTTP/1, HTTP/2, WebSockets protocols.</h2>

## The fingerprints used in the project are generated from: [fp](https://github.com/gospider007/fp)

# features
* True forward proxy transmission, implemented no differently from an IP proxy server
* Simultaneous support for HTTP, HTTPS, and SOCKS5 proxy protocols on the same port
* Automatic upgrade to HTTP/2
* Simulate TLS fingerprints, HTTP/2 fingerprints, and Order headers fingerprints
* Parameter configuration via request headers, such as fingerprint settings and proxy settings
* TCP stream compression, supporting zstd, br, gzip, deflate, snappy, minlz, and other algorithms to reduce bandwidth usage
* Request body compression, enforcing server support for zstd, br, gzip, deflate, and other compressed responses to reduce bandwidth usage


# Fingerproxy CLI Usage
<center>

| Flag                     | Description                            |
| ------------------------ | -------------------------------------- |
| `-mimt-root-cert string` | Path to the MITM root certificate file |
| `-mimt-root-key string`  | Path to the MITM root key file         |
</center>

# headers key table
<center>

| headers key |headers value |
| --- | --- |
| `Gospider007-Fingerproxy-Spec` | Browser fingerprint with [fp](https://github.com/gospider007/fp) |
| `Gospider007-Fingerproxy-Proxy` | ip proxy |
| `Gospider007-Fingerproxy-SpecId` | Fingerprint configuration |
</center>

## Gospider007-Fingerproxy-SpecId
<center>

| Gospider007-Fingerproxy-SpecId | Browser | Platform |
| --- | --- | --- |
| Chrome_Mac_arm64_137 | Chrome | Mac |
| Firefox_Mac_arm64_140 | Firefox | Mac |
| Safari_Mac_arm64_18 | Safari | Mac |

</center>

# quick start
## Installation
### github
```bash
pip install --force-reinstall git+https://github.com/gospider007/fingerproxy.git
```
### gitee
```bash
pip install --force-reinstall git+https://gitee.com/gospider007/fingerproxy.git
```

## Run FingerProxy
```
fingerproxy
```
## Stop FingerProxy
```
fingerproxy_stop
```
## Example Output:
```
listening on: 127.0.0.1:8080
```
## Uninstall
```bash
pip uninstall fingerproxy
```



# Once the server is running on http://127.0.0.1:8080, you can make requests using any HTTP client:
### curl
```bash
curl -k "https://tools.scrapfly.io/api/fp/anything" \
     -x "http://127.0.0.1:8080" \
     -H "Gospider007-Fingerproxy-SpecId: Chrome_Mac_arm64_137"
```
### python
```python
import requests

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080',
}

headers = {
    'Gospider007-Fingerproxy-SpecId': 'Chrome_Mac_arm64_137',
}

response = requests.get('https://tools.scrapfly.io/api/fp/anything', headers=headers, proxies=proxies, verify=False)
print(response.text)
```

### golang
```go
package main

import (
	"crypto/tls"
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"
)

func main() {
	req, _ := http.NewRequest("GET", "https://tools.scrapfly.io/api/fp/anything", nil)
	req.Header.Set("Gospider007-Fingerproxy-SpecId", "Chrome_Mac_arm64_137")
	resp, err := (&http.Client{Transport: &http.Transport{
		Proxy: func(r *http.Request) (*url.URL, error) {
			return url.Parse("http://127.0.0.1:8080")
		},
		TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
	}}).Do(req)
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()
	bodyText, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("%s\n", bodyText)
}
```
### nodejs
```js
import axios from 'axios';

const response = await axios.get('https://tools.scrapfly.io/api/fp/anything', {
  headers: {
    'Gospider007-Fingerproxy-SpecId': 'Chrome_Mac_arm64_137'
  },
  proxy: {
    protocol: 'http',
    host: '127.0.0.1',
    port: 8080
  }
});
console.log(response.data)
```
### php
```php
<?php
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, 'https://tools.scrapfly.io/api/fp/anything');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'GET');
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Gospider007-Fingerproxy-SpecId: Chrome_Mac_arm64_137',
]);
curl_setopt($ch, CURLOPT_PROXY, 'http://127.0.0.1:8080');
curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);

$response = curl_exec($ch);
// 打印响应内容
if ($response === false) {
    echo 'Curl error: ' . curl_error($ch);
} else {
    echo $response;
}
curl_close($ch);
```

# Contributing
If you have a bug report or feature request, you can [open an issue](../../issues/new)
# Contact
If you have questions, feel free to reach out to us in the following ways:
* QQ Group (Chinese): 939111384 - <a href="http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=yI72QqgPExDqX6u_uEbzAE_XfMW6h_d3&jump_from=webapi"><img src="https://pub.idqqimg.com/wpa/images/group.png"></a>
* WeChat (Chinese): gospider007

## Sponsors
If you like and it really helps you, feel free to reward me with a cup of coffee, and don't forget to mention your github id.
<table>
    <tr>
        <td align="center">
            <img src="https://github.com/gospider007/tools/blob/master/play/wx.jpg?raw=true" height="200px" width="200px"   alt=""/>
            <br />
            <sub><b>Wechat</b></sub>
        </td>
        <td align="center">
            <img src="https://github.com/gospider007/tools/blob/master/play/qq.jpg?raw=true" height="200px" width="200px"   alt=""/>
            <br />
            <sub><b>Alipay</b></sub>
        </td>
    </tr>
</table>

## License  
This project is licensed under the Mozilla Public License 2.0 (MPL-2.0) with additional author attribution requirements.  
See the [LICENSE](./LICENSE) file for details.  






