FROM nginx
COPY ./src /usr/share/nginx/html
# support running as arbitrary user which belogs to the root group
RUN chmod g+rwx /var/cache/nginx /var/run /var/log/nginx
# users are not allowed to listen on priviliged ports
RUN sed -i.bak 's/listen\(.*\)80;/listen {{cookiecutter.netapp_port}};/' /etc/nginx/conf.d/default.conf
EXPOSE {{cookiecutter.netapp_port}}
# comment user directive as master process is run as user in OpenShift anyhow
RUN sed -i.bak 's/^user/#user/' /etc/nginx/nginx.conf