#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bincrafters import build_shared
from bincrafters import build_template_default

def add_gflags_shared(build):
    if build_shared.is_shared():
        shared_option_name = "%s:shared" % build_shared.get_name_from_recipe()
        build.options.update({'gflags:shared' : build.options[shared_option_name]})
    return build
    
if __name__ == "__main__":

    builder = build_template_default.get_builder()
    
    builder.builds = map(add_gflags_shared, builder.items)

    builder.run()
