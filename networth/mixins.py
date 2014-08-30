__author__ = 'heddevanderheide'


class NetworthMixin(object):
    def get_default_networth(self):
        return 1

    def networth(self, realtime=True, commit=False):
        return self.__networth(commit=commit)

    def __networth(self, commit=False):
        n = self.get_default_networth()

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
                    if v:
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
            self._commit('_networth', n)

        return n

    def _commit(self, field, value):
        raise NotImplementedError