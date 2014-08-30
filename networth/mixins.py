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

            condition, award = values
            condition_is_callable, award_is_callable = callable(condition), callable(award)

            if condition_is_callable:

                if values[1] == 'result':
                    n += condition(v)

                elif award_is_callable:
                    n += award(condition(v))

                else:
                    if v:
                        n += award

            else:

                if type(condition) == bool:
                    if award_is_callable:
                        n += award(1 if bool(v) == condition else 0)
                    else:
                        n += award

                elif award == 'result':
                    n += v

                elif award_is_callable:
                    n += award(v)

                else:
                    n += award

        if commit:
            self._commit('_networth', n)

        return n

    def _commit(self, field, value):
        raise NotImplementedError