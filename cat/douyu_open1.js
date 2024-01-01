import { Crypto, load, _ } from 'assets://js/lib/cat.js';

let key = 'douyu';
let host = 'http://live.yj1211.work';
let siteKey = '';
let siteType = 0;

const MOBILE_UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36';

async function requestRaw(reqUrl, redirect) {
    let resRaw = await req(reqUrl, {
        method: 'get',
        headers: {
            'User-Agent': MOBILE_UA,
        },
        redirect: redirect,
    });
    return resRaw;
}

async function request(reqUrl) {
    let resRaw = await requestRaw(reqUrl, 1)
    return resRaw.content;
}

// cfg = {skey: siteKey, ext: extend}
async function init(cfg) {

}

async function home(filter) {
    const classes = [
        { type_id: "xingxiu", type_name: "星秀" },
        { type_id: "ecy", type_name: "二次元" },
        { type_id: "yqk", type_name: "一起看" },
        { type_id: "rmyx", type_name: "网游竞技" },
        { type_id: "ip", type_name: "原创IP" },
    ];
    const filterObj = {};
    return JSON.stringify({
        class: _.map(classes, (cls) => {
            cls.land = 1;
            cls.ratio = 1.78;
            return cls;
        }),
        filters: filterObj,
    });
}

async function homeVod() {
    const data = JSON.parse(await request('https://m.douyu.com/api/room/list?type=xingxiu&page=1'));
    let videos = _.map(data.data.list, (it) => {
        return {
           vod_id: it.rid,
            vod_name: it.roomName,
            vod_pic: it.roomSrc,
            vod_remarks: '👁' + it.hn + '　' + '🆙' + it.nickname,
        }
    });
    return JSON.stringify({
        list: videos,
    });
}

async function category(tid, pg, filter, extend) {
    if (pg <= 0 || typeof pg == 'undefined') pg = 1;
    const data = JSON.parse(await request('https://m.douyu.com/api/room/list?type=' + tid + '&page=' + pg));
    let videos = _.map(data.data.list, (it) => {
        return {
            vod_id: it.rid,
            vod_name: it.roomName,
            vod_pic: it.roomSrc,
            vod_remarks: '👁' + it.hn + '　' + '🆙' + it.nickname,
        }
    });
    return JSON.stringify({
        page: parseInt(pg),
        pagecount: 9999,
        limit: 90,
        total: 999999,
        list: videos,
    });
}

async function detail(id) {
    const data = JSON.parse(await request(host + '/api/live/getRoomInfo?platform=douyu&roomId=' + id));
    const video = data.data;
    let vod = {
        vod_id: video.roomId,
        vod_name: video.roomName,
        vod_pic: video.roomPic,
        vod_remarks: video.categoryName,
        type_name: video.categoryName,
        vod_director: video.ownerName,
        vod_actor: '在线人数:' + video.online,
        vod_content: "",
        vod_year: "",
        vod_area: "",   
    };
    vod.vod_play_from = video.platForm;
    vod.vod_play_url = '原画$' + id;
    return JSON.stringify({
        list: [vod],
    });
}

async function play(flag, id, flags) {
    // const resp = await requestRaw('https://getplayurl.lmteam.repl.co/live?platform=douyu&rid=' + id, 0);
    const resp = JSON.parse(await request('http://live.yj1211.work:8013/api/live/getRealUrlMultiSource?platform=douyu&roomId=' + id));

    const headers = resp.data;
    let url = "";
    if (headers.hasOwnProperty('线路5')) {
        url = headers.线路5[0].playUrl;
    }
    return JSON.stringify({
        parse: 0,
        url: url,
        
    });
}

async function search(wd, quick) {
    return '{}';
}

export function __jsEvalReturn() {
    return {
        init: init,
        home: home,
        homeVod: homeVod,
        category: category,
        detail: detail,
        play: play,
        search: search,
    };
}