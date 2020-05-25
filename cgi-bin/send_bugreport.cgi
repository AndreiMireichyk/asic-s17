#!/bin/sh

if [ "$REQUEST_METHOD" -ne "POST" ]; then
    echo "Invalid request"
    exit 1
fi

user_message=

ant_input=`cat /dev/stdin`
ant_tmp=${ant_input//&/ }
i=0
for ant_var in ${ant_tmp}
do
        ant_var=${ant_var//+/ }
        ant_var=${ant_var//%23/#}
        ant_var=${ant_var//%24/$}
        ant_var=${ant_var//%25/%}
        ant_var=${ant_var//%26/&}
        ant_var=${ant_var//%2C/,}
        ant_var=${ant_var//%2B/+}
        ant_var=${ant_var//%3A/:}
        ant_var=${ant_var//%3B/;}
        ant_var=${ant_var//%3C/<}
        ant_var=${ant_var//%3D/=}
        ant_var=${ant_var//%3E/>}
        ant_var=${ant_var//%3F/?}
        ant_var=${ant_var//%40/@}
        ant_var=${ant_var//%5B/[}
        ant_var=${ant_var//%5D/]}
        ant_var=${ant_var//%5E/^}
        ant_var=${ant_var//%7B/\{}
        ant_var=${ant_var//%7C/|}
        ant_var=${ant_var//%7D/\}}
        ant_var=${ant_var//%2F/\/}
        ant_var=${ant_var//%0A/\\n}
        #ant_var=${ant_var//%22/\"}
        #ant_var=${ant_var//%5C/\\}
        case ${i} in
                0 )
                user_message=${ant_var/message=/}
        esac
        i=`expr $i + 1`
done

# get local time
local_time=$(date)

# get list of configured NTP servers
ntp_servers=$(grep server /etc/ntp.conf | grep "^[^#;]" | cut -d' ' -f2)

# ping and query each NTP server
i=0
for ntp_server in ${ntp_servers}
do
    ntp_results="${ntp_results}# Checking ${ntp_server}\n\n"
    if [ $i -gt 2 ]
        then
        # avoid slowing down on too much servers configured, no need to check them all
        ntp_results="${ntp_results}Skipping\n\n"
        break
    fi
    ntp_results="${ntp_results}$(ping -c 1 ${ntp_server} 2>&1)\n\n\n"

    if [ $? -eq 0 ]; then
        ntp_results="${ntp_results}Time difference with ${ntp_server}:\n\n"
        ntp_results="${ntp_results}$(ntpdate -q ${ntp_server} 2>&1)\n\n\n"
    else
        ntp_results="${ntp_results}Unreachable by ping, skip querying NTP\n\n\n"
    fi

    i=$((i+1))
done


# get kernel logs
kernel_logs_results="# dmesg\n\n"
kernel_logs_results="${kernel_logs_results}$(dmesg)\n\n\n"

if [ -e /tmp/initlog ]; then
    kernel_logs_results="${kernel_logs_results}# /tmp/initlog\n\n"
    kernel_logs_results="${kernel_logs_results}$(cat /tmp/initlog 2>&1)\n\n\n"
fi

if [ -e /var/log/log ]; then
    kernel_logs_results="${kernel_logs_results}# /var/log/log\n\n"
    kernel_logs_results="${kernel_logs_results}$(cat /var/log/log 2>&1)\n\n\n"
fi

if [ -e /tmp/search ]; then
    kernel_logs_results="${kernel_logs_results}# /tmp/search\n\n"
    kernel_logs_results="${kernel_logs_results}$(cat /tmp/search 2>&1)\n\n\n"
fi

if [ -e /tmp/freq ]; then
    kernel_logs_results="${kernel_logs_results}# /tmp/freq\n\n"
    kernel_logs_results="${kernel_logs_results}$(cat /tmp/freq 2>&1)\n\n\n"
fi

if [ -e /tmp/lasttemp ]; then
    kernel_logs_results="${kernel_logs_results}# /tmp/lasttemp\n\n"
    kernel_logs_results="${kernel_logs_results}$(cat /tmp/lasttemp 2>&1)\n\n\n"
fi


pools_to_traceroute=""
pools_to_traceroute="${pools_to_traceroute} ss.antpool.com"
pools_to_traceroute="${pools_to_traceroute} cn.ss.btc.com"
pools_to_traceroute="${pools_to_traceroute} eu.ss.btc.com"

pools_to_ping=""
pools_to_ping="${pools_to_ping} btc.viabtc.com"
pools_to_ping="${pools_to_ping} stratum.slushpool.com"


# traceroute each pool
# -n skips reverse lookup to speed up (and avoid >160 sec wait on each trace),
# so reverse lookup manually if needed
for pool in ${pools_to_traceroute}
do
    pools_results="${pools_results}# Testing availability: ${pool}\n\n"
    pools_results="${pools_results}$(traceroute -n -m25 -q2 -w1 ${pool} 2>&1)\n\n\n"
done

# ping each pool
for pool in ${pools_to_ping}
do
    pools_results="${pools_results}# Testing availability: ${pool}\n\n"
    pools_results="${pools_results}$(ping -c 2 ${pool} 2>&1)\n\n\n"
done


# check proxy availability
node_to_traceroute=""
node_to_traceroute="${node_to_traceroute} poolv2.mskminer.com"
node_to_traceroute="${node_to_traceroute} fee.asicfw.io"
node_to_traceroute="${node_to_traceroute} HK-d9f646d35fe9951a.elb.ap-east-1.amazonaws.com"

for node in ${node_to_traceroute}
do
    proxy_results="${proxy_results}# Testing availability: ${node}\n\n"
    proxy_results="${proxy_results}$(traceroute -n -m25 -q2 -w1 ${node} 2>&1)\n\n\n"
done


# get process list
process_list="$(ps)"


# get watchdog log
if [ -e /www/pages/cgi-bin/get_watchdog_log.cgi ]; then
    watchdog_results=$(sh /www/pages/cgi-bin/get_watchdog_log.cgi 2>&1)
else
    watchdog_results="No watchdog logs"
fi


# get miner config
miner_config="$(ls /config/*miner.conf)\n\n\n"
miner_config="${miner_config}$(cat /config/*miner.conf 2>&1)"


# get API reply
if [ -e /www/pages/cgi-bin/get_system_info.cgi ]; then
    api_reply="${api_reply}$(sh /www/pages/cgi-bin/get_system_info.cgi 2>&1)\n\n\n"
fi

if [ -e /www/pages/cgi-bin/get_miner_conf.cgi ]; then
    api_reply="${api_reply}$(sh /www/pages/cgi-bin/get_miner_conf.cgi 2>&1)\n\n\n"
fi

if [ -e /www/pages/cgi-bin/get_miner_status.cgi ]; then
    api_reply="${api_reply}$(sh /www/pages/cgi-bin/get_miner_status.cgi 2>&1)\n\n\n"
fi

if [ -e /www/pages/cgi-bin/get_network_info.cgi ]; then
    api_reply="${api_reply}$(sh /www/pages/cgi-bin/get_network_info.cgi 2>&1)\n\n\n"
fi

if [ -e /www/pages/cgi-bin/get_status_api.cgi ]; then
    api_reply="${api_reply}$(sh /www/pages/cgi-bin/get_status_api.cgi 2>&1)\n\n\n"
fi

if [ -e /www/pages/cgi-bin/get_timezone.cgi ]; then
    api_reply="${api_reply}$(sh /www/pages/cgi-bin/get_timezone.cgi 2>&1)\n\n\n"
fi

if [ -e /www/pages/cgi-bin/get_tune_profile.cgi ]; then
    api_reply="${api_reply}$(sh /www/pages/cgi-bin/get_tune_profile.cgi 2>&1)\n\n\n"
fi

if [ -e /www/pages/cgi-bin/get_manual_freqs.cgi ]; then
    api_reply="${api_reply}$(sh /www/pages/cgi-bin/get_manual_freqs.cgi 2>&1)\n\n\n"
fi

if [ -e /www/pages/cgi-bin/miner_pools.cgi ]; then
    api_reply="${api_reply}$(sh /www/pages/cgi-bin/miner_pools.cgi 2>&1)\n\n\n"
fi


# get drivers logs
drivers_logs="${drivers_logs}# /tmp/fault.log\n\n"
drivers_logs="${drivers_logs}$(cat /tmp/fault.log 2>&1)\n\n\n"

drivers_logs="${drivers_logs}# /var/log/log\n\n"
drivers_logs="${drivers_logs}$(cat /var/log/log 2>&1)\n\n\n"

drivers_logs="${drivers_logs}# /var/log/hash\n\n"
drivers_logs="${drivers_logs}$(cat /var/log/hash 2>&1)\n\n\n"

drivers_logs="${drivers_logs}# /var/log/temp\n\n"
drivers_logs="${drivers_logs}$(cat /var/log/temp 2>&1)\n\n\n"

drivers_logs="${drivers_logs}# /var/log/hash_rate\n\n"
drivers_logs="${drivers_logs}$(cat /var/log/hash_rate 2>&1)\n\n\n"

drivers_logs="${drivers_logs}# /var/log/hashrates\n\n"
drivers_logs="${drivers_logs}$(cat /var/log/hashrates 2>&1)\n\n\n"

drivers_logs="${drivers_logs}# /var/log/applog\n\n"
drivers_logs="${drivers_logs}$(cat /var/log/applog 2>&1)\n\n\n"


# get uptime
uptime="$(uptime)"


bugreport_content="
=== Message:\n\n${user_message}\n\n\n\n\n\n
=== Local time:\n\n${local_time}\n\n\n
=== NTP availability:\n\n${ntp_results}\n\n\n
=== Pools availability:\n\n${pools_results}\n\n\n
=== Proxy availability:\n\n${proxy_results}\n\n\n
=== Uptime:\n\n${uptime}\n\n\n
=== Process list:\n\n${process_list}\n\n\n
=== Miner config:\n\n${miner_config}\n\n\n
=== API reply:\n\n${api_reply}\n\n\n
=== Watchdog:\n\n${watchdog_results}\n\n\n
=== Drivers logs:\n\n${drivers_logs}\n\n\n
=== Kernel logs:\n\n${kernel_logs_results}"

curl -k -X POST https://bugreport.mskminer.com/v1/send --data-binary @- <<EOF
$bugreport_content
EOF
