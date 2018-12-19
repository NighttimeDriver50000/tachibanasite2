/*
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.

Copyright 2016 Chris McKinney.
*/

function deobfuscateEmail(t, mailto) {
    t = decodeURIComponent(t);
    s = '';
    for (var i = 0; i < t.length; ++i) {
        var c = t.charCodeAt(i);
        if (mailto) {
            s += String.fromCharCode(c ^ 0x1f);
        } else {
            s += '&#' + (c ^ 0x1f) + ';<span style="display:none">@</span>';
        }
    }
    return s;
}

window.addEventListener("load", function(event) {
    var emailRegex = /^@@([jkhinolmbc]{4})<code>([%\/_.\-a-zA-Z0-9]+)<\/code>\1@@$/;
    $('a, .email').each(function() {
        var href = $(this).attr('href');
        var hrefm = emailRegex.exec(href);
        if (hrefm != null) {
            $(this).attr('href', deobfuscateEmail(hrefm[2], true));
        }
        var html = $(this).html();
        var htmlm = emailRegex.exec(html);
        if (htmlm != null) {
            $(this).html(deobfuscateEmail(htmlm[2], false));
        }
    });
});
