from contextlib import contextmanager


stack = []


class ContextManager(object):

    def __getattr__(self, name):
        for ctx in reversed(stack):
            if hasattr(ctx, name):
                return getattr(ctx, name)
        raise AttributeError(name)

    def __setattr__(self, name, value):
        top = stack[-1]
        setattr(top, name, value)


class Context(dict):

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value


@contextmanager
def new_context(**kwargs):
    ctx = Context()
    ctx.update(kwargs)
    stack.append(ctx)
    try:
        yield ctx
    finally:
        stack.pop()


cur_context = ContextManager()
