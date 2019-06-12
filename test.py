# ===============================================================================
# Copyright 2019 ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================

import string
import sys
import time

seeds = string.ascii_uppercase
ALPHAS = [a for a in seeds] + ['{}{}'.format(a, b)
                               for a in seeds
                               for b in seeds]

ALPHAS_S = seeds + ''.join(('{}{}'.format(a, b)
                            for a in seeds
                            for b in seeds))

# def alpha_to_int(s):
#     i = -1
#     if s:
#         if s in seeds:
#             i = seeds.index(s)
#         else:
#
#             i = 0
#             k = 0
#             for j, se in enumerate(reversed(s)):
#                 base = 26**j
#                 i += (seeds.index(se)+k)*base
#                 k = 1
#
#             # i = (seeds.index(s[0])+1)*26+seeds.index(s[1])
#
#     return i
#
#
# def alpha_to_int2(s):
#     return ALPHAS.index(s)
#
#
# def alphas(idx):
#     """
#         idx should be 0-base ie. idx=0 ==>A
#     """
#     idx = int(idx)
#     if idx >= 0:
#         if idx < 26:
#             return seeds[idx]
#         else:
#             s = ''
#             while idx:
#                 a = idx//26 - 1
#                 print('aasd', idx, a)
#                 s += seeds[a]
#                 idx = idx - a
#                 print(idx, a)
#                 time.sleep(0.5)
#
#             return s
#
#             # a = idx // 26 - 1
#             # b = idx % 26
#             # return '{}{}'.format(seeds[a], seeds[b])

'https://codereview.stackexchange.com/questions/182733/base-26-letters-and-base-10-using-recursion'
BASE = 26
A_UPPERCASE = ord('A')


def alphas(n):
    a = ''
    if n is not None and n >= 0:
        def decompose(n):
            while n:
                n, rem = divmod(n, BASE)
                yield rem

        digits = reversed([chr(A_UPPERCASE + part) for part in decompose(n)])
        a = ''.join(digits)
    return a


def alpha_to_int(l):
    return sum((ord(li) - A_UPPERCASE) * BASE ** i for i, li in enumerate(reversed(l.upper())))


if __name__ == '__main__':
    a = ALPHAS[3]
    # print(sys.getsizeof(ALPHAS))
    # print(sys.getsizeof(ALPHAS_S))
    print(ALPHAS_S.index('A'), ALPHAS.index('A'))
    print(ALPHAS_S.index('Z'), ALPHAS.index('Z'))
    print(ALPHAS_S.index('AA'), ALPHAS.index('AA'))
    print(ALPHAS_S.index('AB'), ALPHAS.index('AB'))
    # print(a)

    # print(alpha_to_int2('A'), alpha_to_int2('AA'), alphas(alpha_to_int2('AA')))
    #
    # print(alpha_to_int('A'), alpha_to_int('AA'), alphas(alpha_to_int('AA')))
    # print(alpha_to_int('D'), alpha_to_int('AA'), alphas(alpha_to_int('AA')))
    # print(alpha_to_int('D'), alpha_to_int('DD'), alphas(alpha_to_int('DD')))
    print(alpha_to_int('D'), alpha_to_int('DDD'), alphas(alpha_to_int('DDD')))
    print(alpha_to_int('A'), alpha_to_int('DDD'), alphas(alpha_to_int('DDD')))
    # print(alpha_to_int(''), alphas(alpha_to_int('')))
    print('a={}'.format(alphas(None)), 'b={}'.format(alphas(-1)))
# ============= EOF =============================================
