import inspect


class Lifecycle:
    """
    This class holds a lifecycle hook.

    This mean that before each event: before processing files, after
    processing files, etc. etc. Each class flow that want to have a life cycle
    hook will extend this class and will the methods which match the content
    of the event. For example:

    self.pre_action('get_files', files=files)
    files = self.get_files()
    self.post_action('get_files', files=files)

    for file in files:
        self.pre_action('process_file', file=file)
        move_file_to_db(file)
        self.post_action('process_file', file=file)


    For interacting with the flow you can override the method and do what you
    want to do. in other case you can implement a method which goes by the
    name hook_METHOD_NAME. For example:

    def hook_pre_get_files(files):
        pass

    def hook_post_get_files(files):
        pass

    The word "hook" in the name of method exists just to be clear that this is
    a lifecycle hook.
    """

    def pre_action(self, event, **kwargs):
        # Check if there is method with the name hook_pre_event and trigger
        # it.
        method_name = f'hook_pre_{event}'
        if hasattr(self, method_name):
            if inspect.ismethod(getattr(self, method_name)):
                reference = getattr(self, method_name)
                reference(**kwargs)

    def post_action(self, event, **kwargs):
        # Check if there is method with the name hook_post_event and trigger
        # it.
        method_name = f'hook_post_{event}'
        if hasattr(self, method_name):
            if inspect.ismethod(getattr(self, method_name)):
                reference = getattr(self, method_name)
                reference(**kwargs)
