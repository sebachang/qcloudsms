# -*- coding: utf-8 -*-

base_template = """
user              nginx;
worker_processes  auto;
worker_cpu_affinity auto;

error_log  /data/applog/openresty/error.log;

pid        /data/app/openresty-moonton/openresty.pid;
worker_rlimit_nofile 65535;

#加载动态模块
include /data/app/openresty-moonton/nginx/conf/modules/*.conf;

events {
    use epoll;
    worker_connections  65535;
}


http {
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    log_format proxy_json '{ "@timestamp": "$time_iso8601", '
                             '"site_name": "$host", '
                             '"remote_addr": "$remote_addr", '
                             '"remote_user": "$remote_user", '
                             '"http_user_agent": "$http_user_agent", '
                             '"referer": "$http_referer", '
                             '"request_method": "$request_method", '
                             '"request_uri": "$request_uri", '
                             '"server_protocol": "$server_protocol", '
                             '"request_time": "$request_time", '
                             '"request_length": "$request_length", '
                             '"request_body": "$request_body", '
                             '"status": $status, '
                             '"body_bytes_sent": $body_bytes_sent, '
                             '"x_forwarded": "$http_x_forwarded_for", '
                             '"upstream_addr": "$upstream_addr",'
                             '"upstream_host": "$upstream_http_host",'
                             '"upstream_status": "$upstream_status", '
                             '"upstream_resp_time": "$upstream_response_time",'
                             '"upstream_cache_status": "$upstream_cache_status"'
                         ' }';

    access_log  /data/applog/openresty/access.log  main;

    include       mime.types;
    default_type  application/octet-stream;

    server_tokens       	off;
    sendfile            	on;
    tcp_nopush          	on;
    tcp_nodelay         	on;
    keepalive_timeout   	65;
    client_max_body_size        3m;
    types_hash_max_size 	2048;

    fastcgi_connect_timeout 300;
    fastcgi_send_timeout 300;
    fastcgi_read_timeout 300;
    fastcgi_buffer_size 1024k;
    fastcgi_buffers 32 1024k;
    fastcgi_busy_buffers_size 2048k;
    fastcgi_temp_file_write_size 2048k;
    fastcgi_ignore_client_abort on;

    gzip  on;
    gzip_disable "MSIE [1-6]."; # 禁用IE6的gzip压缩
    gzip_min_length 1k; # 最小压缩长度
    gzip_proxied any; #对所有的请求启用压缩
    gzip_buffers 4 16k; # 以原始数据大小4倍，以16k为单位申请内存
    gzip_comp_level 3; # 1-9，1压缩比最小处理速度最快，9相反
    gzip_types text/plain application/x-javascript application/javascript text/css application/xml text/javascript image/jpeg image/gif image/png; # 对html/css/xml/js等提供压>缩
    gzip_vary on; # 根据http头判断是否需要压缩

   {% if  certificate.exist %}
    ssl_certificate  /data/app/openresty-moonton/nginx/conf/ssl/{{certificate.domain}}/{{certificate.name}}.crt;
    ssl_certificate_key  /data/app/openresty-moonton/nginx/conf/ssl/{{certificate.domain}}/{{certificate.name}}.key;
    ssl_session_cache  shared:SSL:10m;
    ssl_session_timeout  10m;
    ssl_protocols  TLSv1;
    ssl_ciphers  ALL:!ADH:!EXPORT56:RC4+RSA:+HIGH:+MEDIUM:+LOW:+SSLv2:+EXP;
    ssl_prefer_server_ciphers  on;
   {%- endif %}

   {% for key, value in upstream.items() %}
	upstream {{key}} {
	   {%- for row in value %}
	    server {{row.ip}}:{{row.port}} weight={{row.weight}}  max_fails={{row.max_fails}} fail_timeout={{row.fail_timeout}}s;
       {%- endfor %}
	}      
   {% endfor %}

   {%- for vhost in vhosts %}
    server {
        {%- if  vhost.ssl %}
        listen {{vhost.port}} ssl http2;
        {%- else %}
        listen {{vhost.port}} http2;
        {%- endif %} 
        server_name {{vhost.domain}};
        root {{vhost.root}};
        index {{vhost.index}};
        access_log /data/applog/openresty/{{vhost.domain}}.log proxy_json;

        if ($host != {{vhost.domain}}) {
            rewrite ^/(.*)$ $scheme://{{vhost.domain}}/$1 permanent;
        }

        {%- for location in vhost.locations %}
        {% if  location.match %}
        location  {{location.match}} {{location.path}}{
        {%- else %}
        location  {{location.path}} {
        {%- endif %} 
            {%- if  location.proxy %}
             proxy_pass  {{location.proxy_scheme}}://{{location.proxy}};
             proxy_set_header Host $host;
             proxy_set_header X-Forwarded-For $remote_addr;
             proxy_redirect off;
             proxy_connect_timeout 90;
             proxy_send_timeout 90;
             proxy_read_timeout 90;
             proxy_buffer_size 4k;
             proxy_buffers 4 64k;
             proxy_busy_buffers_size 128k;
             proxy_temp_file_write_size 128k;
            {%- else %}
            root {{location.root}};
            index {{location.index}};
            {%- endif %}
         }   
        {%- endfor %}
    }
   {% endfor %}
}
"""