// 测试开发
// const baseurl = 'http://192.168.39.124:8009/'
// const wsurl = 'ws://192.168.39.124:8009/'

// 正式服务器
// const baseurl = 'https://wms25.czlingyue.com/'
// const wsurl = 'wss://wms25.czlingyue.com/websocket/'

// 不走cdn
// const baseurl = 'http://cb.czhaoling.com:18080/'
// const wsurl = 'ws://cb.czhaoling.com:18080/websocket/'

// 正式环境
var w_location = window.location
var w_schema = w_location.protocol
var w_host = w_location.host
const baseurl = w_schema + '//' + w_host + '/'
const wsurl = 'wss://' + w_host + '/websocket/'
window.g = {
  BaseUrl: baseurl,
  WsUrl: wsurl
}
