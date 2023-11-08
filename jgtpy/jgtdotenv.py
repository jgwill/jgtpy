

# class JGTDotenv(dict):
#     def __init__(self, file_path):
#         self.file_path = file_path
#         super(JGTDotenv, self).__init__(**self.__create_dict())

#     def __create_dict(self):
#         with open(self.file_path, 'r') as jgtdotenv:
#             variables = {}
#             for line in jgtdotenv.readlines():
#                 variables.update(self.__parse_line(line))
#             return variables

#     def __parse_line(self, line):
#         if line.lstrip().startswith('#'):
#             # discard and return nothing
#             return {}
#         if line.lstrip():
#             # find the second occurence of a quote mark:
#             quote_delimit = max(line.find('\'', line.find('\'') + 1),
#                                 line.find('"', line.rfind('"')) + 1)
#             # find first comment mark after second quote mark
#             comment_delimit = line.find('#', quote_delimit)
#             line = line[:comment_delimit]
#             key, value = map(lambda x: x.strip().strip('\'').strip('"'),
#                              line.split('=', 1))
#             return {key: value}
#         else:
#             return {}

#     def __persist(self):
#         with open(self.file_path, 'w') as jgtdotenv:
#             for key, value in self.items():
#                 jgtdotenv.write("%s=%s\n" % (key, value))

#     def __setitem__(self, key, value):
#         super(JGTDotenv, self).__setitem__(key, value)
#         self.__persist()

#     def __delitem__(self, key):
#         super(JGTDotenv, self).__delitem__(key)
#         self.__persist()


# def set_variable(file_path, key, value):
#     jgtdotenv = JGTDotenv(file_path)
#     jgtdotenv[key] = value


# def get_variable(file_path, key):
#     jgtdotenv = JGTDotenv(file_path)
#     return jgtdotenv[key]


# def get_variables(file_path):
#     return JGTDotenv(file_path)




# # # encoding=UTF-8

# # from __future__ import with_statement


# # __versionjgtdotenv__ = '0.0.5'
# # import argparse
# # #from jgtdotenv import get_variable, set_variable, get_variables, __version__


# # parser = argparse.ArgumentParser()

# # parser.add_argument("key", nargs='?')
# # parser.add_argument("value", nargs='?')

# # parser.add_argument('--file', default='.env')

# # parser.add_argument('--version', action='version', version=__version__)

# # parser.add_argument('--shell', action='store_true', default=False)

# # args = parser.parse_args()


# # if args.shell:
# #     PRINT_FORMAT = '%s=%s'
# # else:
# #     PRINT_FORMAT = '%s: %s'

# # if args.key is None:
# #     for key, value in get_variables(args.file).items():
# #         print(PRINT_FORMAT % (key, value))
# # elif args.value is None:
# #     print(PRINT_FORMAT % (args.key, get_variable(args.file, args.key)))
# # else:
# #     set_variable(args.file, args.key, args.value)
# #     print(PRINT_FORMAT % (args.key, args.value))

