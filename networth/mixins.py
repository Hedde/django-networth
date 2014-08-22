__author__ = 'heddevanderheide'


class NetworthMixin(object):
    def networth(self, commit=False):
        return self._networth(commit=commit)

    def _networth(self, commit=False):
        n = 0

        for field in self.__class__.Networth.fields:
            f, values = field

            v = getattr(self, f)

            definition, points = values
            definition_is_callable, points_is_callable = callable(definition), callable(points)

            if definition_is_callable:

                if values[1] == 'result':
                    n += definition(v)

                elif points_is_callable:
                    n += points(definition(v))

                else:
                    n += points

            else:

                if type(definition) == bool:
                    if points_is_callable:
                        n += points(1 if bool(v) == definition else 0)
                    else:
                        n += points

                elif points == 'result':
                    n += v

                elif points_is_callable:
                    n += points(v)

                else:
                    n += points

        if commit:
            self._commit(n)

        return n

    def _commit(self, n):
        raise NotImplementedError