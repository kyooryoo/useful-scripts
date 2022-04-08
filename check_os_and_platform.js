var userAgent = window.navigator.userAgent,
    // navigator?.platform is deprecated
    platform = navigator?.userAgentData?.platform || navigator?.platform || 'unknown',
    macosPlatforms = ['Macintosh', 'MacIntel', 'MacPPC', 'Mac68K', 'macOS'],
    windowsPlatforms = ['Win32', 'Win64', 'Windows', 'WinCE'],
    iosPlatforms = ['iPhone', 'iPad', 'iPod'],
    os = null;

if (macosPlatforms.indexOf(platform) !== -1) {
    var os = 'Mac OS';
} else if (iosPlatforms.indexOf(platform) !== -1) {
    os = 'iOS';
    var start = userAgent.indexOf('OS ');
    var end = userAgent.indexOf('like M');
    if ((userAgent.indexOf('iPhone') > -1 || userAgent.indexOf('iPad') > -1) && start > -1) {
        var ver = userAgent.substring(start + 3, end - start - 3).replace(/_/g, '.');
    }
} else if (windowsPlatforms.indexOf(platform) !== -1) {
    var os = 'Windows';
} else if (/Android/.test(userAgent)) {
    var os = 'Android';
    var ua = userAgent.toLowerCase();
    var match = ua.match(/android\s([0-9\.]*)/i);
    var ver = match ? match[1] : undefined;
} else if (!os && /Linux/.test(platform)) {
    var os = 'Linux';
}