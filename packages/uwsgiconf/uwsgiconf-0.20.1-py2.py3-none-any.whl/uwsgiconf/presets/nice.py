from ..config import Section as _Section


class Section(_Section):
    """Basic nice configuration."""

    def __init__(
            self, name=None, touch_reload=None, workers=None, threads=None, mules=None, owner=None,
            log_into=None, log_dedicated=None,
            process_prefix=None, ignore_write_errors=None,
            **kwargs):
        """

        :param str|unicode name: Section name.

        :param str|list touch_reload: Reload uWSGI if the specified file or directory is modified/touched.

        :param int workers: Spawn the specified number of workers (processes).
            Default: workers number equals to CPU count.

        :param int|bool threads: Number of threads per worker or ``True`` to enable user-made threads support.

        :param int mules: Number of mules to spawn.

        :param str|unicode owner: Set process owner user and group.

        :param str|unicode log_into: Filepath or UDP address to send logs into.

        :param bool log_dedicated: If ``True`` all logging will be handled with a separate
            thread in master process.

        :param str|unicode process_prefix: Add prefix to process names.

        :param bool ignore_write_errors: If ``True`` no annoying SIGPIPE/write/writev errors
            will be logged, and no related exceptions will be raised.

            .. note:: Usually such errors could be seen on client connection cancelling
               and are safe to ignore.

        :param kwargs:
        """
        super(Section, self).__init__(strict_config=True, name=name, **kwargs)

        # Fix possible problems with non-ASCII.
        self.env('LANG', 'en_US.UTF-8')

        if touch_reload:
            self.main_process.set_basic_params(touch_reload=touch_reload)

        if workers:
            self.workers.set_basic_params(count=workers)
        else:
            self.workers.set_count_auto()

        set_threads = self.workers.set_thread_params

        if isinstance(threads, bool):
            set_threads(enable=threads)

        else:
            set_threads(count=threads)

        if log_dedicated:
            self.logging.set_master_logging_params(enable=True, dedicate_thread=True)

        self.workers.set_mules_params(mules=mules)
        self.workers.set_harakiri_params(verbose=True)
        self.main_process.set_basic_params(vacuum=True)
        self.main_process.set_naming_params(
            autonaming=True,
            prefix='%s ' % process_prefix if process_prefix else None,
        )
        self.master_process.set_basic_params(enable=True)
        self.master_process.set_exit_events(sig_term=True)  # Respect the convention. Make Upstart and Co happy.
        self.locks.set_basic_params(thunder_lock=True)
        self.configure_owner(owner=owner)
        self.logging.log_into(target=log_into)

        if ignore_write_errors:
            self.master_process.set_exception_handling_params(no_write_exception=True)
            self.logging.set_filters(write_errors=False, sigpipe=False)

    def get_log_format_default(self):
        """Returns default log message format.

        .. note:: Some params may be missing.

        """
        vars = self.logging.vars

        format_default = (
            '[pid: %s|app: %s|req: %s/%s] %s (%s) {%s vars in %s bytes} [%s] %s %s => '
            'generated %s bytes in %s %s%s(%s %s) %s headers in %s bytes (%s switches on core %s)' % (

                vars.WORKER_PID,
                '-',  # app id
                '-',  # app req count
                '-',  # worker req count
                vars.REQ_REMOTE_ADDR,
                vars.REQ_REMOTE_USER,
                vars.REQ_COUNT_VARS_CGI,
                vars.SIZE_PACKET_UWSGI,
                vars.REQ_START_CTIME,
                vars.REQ_METHOD,
                vars.REQ_URI,
                vars.RESP_SIZE_BODY,
                vars.RESP_TIME_MS,  # or RESP_TIME_US,
                '-',  # tsize
                '-',  # via sendfile/route/offload
                vars.REQ_SERVER_PROTOCOL,
                vars.RESP_STATUS,
                vars.RESP_COUNT_HEADERS,
                vars.RESP_SIZE_HEADERS,
                vars.ASYNC_SWITCHES,
                vars.CORE,
        ))

        return format_default

    @classmethod
    def get_bundled_static_path(cls, filename):
        """Returns a full path to a static HTML page file bundled with uwsgiconf.

        :param str filename: File name to return path to.

            Examples:
                * 403.html
                * 404.html
                * 500.html
                * 503.html

        :rtype: str

        """
        from pathlib import Path
        return str(Path(__file__).parent.parent / 'contrib/django/uwsgify/static/uwsgify' / filename)

    def configure_maintenance_mode(self, trigger, response):
        """Allows maintenance mode when a certain response
        is given for every request if a trigger is set.

        :param str trigger: This triggers maintenance mode responses.
            Should be a path to a file: if file exists, maintenance mode is on.

        :param str response: Response to to give in maintenance mode.

            Supported:
                * File path - this file will be served in response.
                * URLs starting with ``http`` - requests will be redirected there using 302.
                  This is often discouraged, because it may have search ranking implications.

        """
        from pathlib import Path

        routing = self.routing

        rule = routing.route_rule

        if response.startswith('http'):
            action = rule.actions.redirect(response)

        else:
            action = rule.actions.serve_static(Path(response).absolute())

        routing.register_route(
            routing.route_rule(
                subject=rule.subjects.custom(trigger).exists(),
                action=action,
            ))

        return self

    def configure_owner(self, owner='www-data'):
        """Shortcut to set process owner data.

        :param str|unicode owner: Sets user and group. Default: ``www-data``.

        """
        if owner is not None:
            self.main_process.set_owner_params(uid=owner, gid=owner)

        return self

    def configure_certbot_https(self, domain, webroot, address=None, allow_shared_sockets=None):
        """Enables HTTPS using certificates from Certbot https://certbot.eff.org.

        .. note:: This relies on ``webroot`` mechanism of Certbot - https://certbot.eff.org/docs/using.html#webroot

            Sample command to get a certificate: ``certbot certonly --webroot -w /webroot/path/ -d mydomain.org``

        :param str domain: Domain name certificates issued for
            (the same as in ``-d`` option in the above command).

        :param str webroot: Directory to store challenge files to get and renew the certificate
            (the same as in ``-w`` option in the above command).

        :param str address: Address to bind socket to.

        :param bool allow_shared_sockets: Allows using shared sockets to bind
            to priviledged ports. If not provided automatic mode is enabled:
            shared are allowed if current user is not root.

        """
        address = address or ':443'

        networking = self.networking

        path_cert_chain, path_cert_private = networking.sockets.https.get_certbot_paths(domain)

        path_cert_chain and networking.register_socket(
            networking.sockets.from_dsn(
                'https://%s?cert=%s&key=%s' % (address, path_cert_chain, path_cert_private),
                allow_shared_sockets=allow_shared_sockets))

        self.statics.register_static_map(
            '/.well-known/', webroot, retain_resource_path=True)

        return self


class PythonSection(Section):
    """Basic nice configuration using Python plugin."""

    def __init__(
            self, name=None, params_python=None, wsgi_module=None, wsgi_callable=None,
            embedded_plugins=True, require_app=True, threads=True, **kwargs):
        """

        :param str|unicode name: Section name.

        :param dict params_python: See Python plugin basic params.

        :param str|unicode wsgi_module: WSGI application module path or filepath.

            Example:
                mypackage.my_wsgi_module -- read from `application` attr of mypackage/my_wsgi_module.py
                mypackage.my_wsgi_module:my_app -- read from `my_app` attr of mypackage/my_wsgi_module.py

        :param str|unicode|callable wsgi_callable: WSGI application callable name. Default: application.

        :param bool|None embedded_plugins: This indicates whether plugins were embedded into uWSGI,
            which is the case if you have uWSGI from PyPI.

        :param bool require_app: Exit if no app can be loaded.

        :param int|bool threads: Number of threads per worker or ``True`` to enable user-made threads support.

        :param kwargs:
        """
        if embedded_plugins is True:
            embedded_plugins = self.embedded_plugins_presets.BASIC + ['python', 'python2', 'python3']

        super(PythonSection, self).__init__(
            name=name, embedded_plugins=embedded_plugins, threads=threads,
            **kwargs)

        self.python.set_basic_params(**(params_python or {}))

        if callable(wsgi_callable):
            wsgi_callable = wsgi_callable.__name__

        self.python.set_wsgi_params(module=wsgi_module, callable_name=wsgi_callable)

        self.applications.set_basic_params(exit_if_none=require_app)
