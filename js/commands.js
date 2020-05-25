function waitAndReload(t) {
    setTimeout(function() {
        window.location.reload();
    }, t);
}

function stopMinerHeader(btn) {
    sendCommandHeader("stop_miner.cgi", null, "GET", btn, true, 20000, "text", false, null);
}

function startMinerHeader(btn) {
    sendCommandHeader("resume_miner.cgi", null, "GET", btn, true, 20000, "text", false, function (a) {if (a.trim() == "not ok") alert("Someone has deleted backup config, please save config on main configuration page with desired mode")});
}

function rebootHeader(btn) {
    sendCommandHeader("reboot.cgi", null, "GET", btn, true, 120000, "text", false, null);
}

function enable_mining(btn) {
    if (confirm("Are you sure that you want to enable mining?")) {
        sendCommandHeader("enable_mining.cgi", null, "GET", btn, false, 20000, "text", false, null);
    }
}

function sendCommandHeader(cmd, data, method, btn, ask, t, type, async, h) {
    if (!ask || confirm("Are you sure?")) {
        jQuery("#refresh").remove();
        if (cmd != "enable_mining.cgi")
            jQuery(btn).append('<img src="/resources/icons/loading.gif" width="15" style="float:right"/>');
        else
            jQuery(btn).append('<img src="/resources/icons/loading.gif" width="20"/>');
        jQuery.ajax({
            url: '/cgi-bin/' + cmd,
            type: method,
            dataType: type,
            timeout: 30000,
            cache: false,
            data: data,
            success: function(data) {
                if (h) h(data);
            },
            error: function() {
            },
            async: async
        });
        waitAndReload(t);
    }
}

function checkBlinkHeader(){
    $.ajax({
        url: '/cgi-bin/blink.cgi',
        type: 'POST',
        dataType: 'json',
        cache: false,
        data: {action: 'onPageLoaded'},
        success: function(data) {
            if (data.isBlinking) {
                $("#stopSearchHeader").show();
                $("#startSearchHeader").hide();
            } else {
                $("#stopSearchHeader").hide();
                $("#startSearchHeader").show();
            }
        },
        error: function(data) {
        }
    });
}

function checkMiningHeader(){
    $.ajax({
        url: '/cgi-bin/check_mining.cgi',
        type: 'POST',
        dataType: 'text',
        cache: false,
        data: "",
        success: function(data) {
            if (data.trim() == "1") {
                $("#stopHeader").show();
                $("#startHeader").hide();
            } else {
                $("#stopHeader").hide();
                $("#startHeader").show();
            }
        },
        error: function(data) {
        }
    });
}

function restartHeader(btn) {
    sendCommandHeader("restart_miner.cgi", null, "GET", btn, true, 2000, "text", false, null);
}

function startSearchHeader(btn) {
    sendCommandHeader("blink.cgi", {action: 'startBlink'}, "POST", btn, false, 2000, "json", true, null);
}

function stopSearchHeader(btn) {
    sendCommandHeader("blink.cgi", {action: 'stopBlink'}, "POST", btn, false, 2000, "json", false, null);
}



$(function(){
    checkBlinkHeader();
    checkMiningHeader();
});

function f_get_info() {
    $.ajax({
        url: '/cgi-bin/get_system_info.cgi',
        type: 'GET',
        dataType: 'json',
        timeout: 30000,
        cache: false,
        success: function (data) {
            try {
                $(".app-header .badge-success").html(data.minertype);
            } catch (err) {
                alert('Invalid system and miner configuration file. Edit manually or reset to default.');
            }
        },
        error: function () {
            //alert('Ajax Error');
        }
    });
}

$(document).ready(function () {
    f_get_info();
});
