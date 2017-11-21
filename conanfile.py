#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class GlogConan(ConanFile):
    name = "glog"
    version = "0.3.5"
    url = "https://github.com/bincrafters/conan-glog"
    description = "Google logging library"
    license = "https://github.com/google/glog/blob/master/COPYING"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=False"
    #use static org/channel for libs in conan-center
    #use dynamic org/channel for libs in bincrafters
    requires = "gflags/[>=2.2]@bincrafters/stable"

    def source(self):
        source_url =  "https://github.com/google/{0}".format(self.name)
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, "sources")
        #Rename to "sources" is a convention to simplify later steps

    def build(self):
        cmake = CMake(self)

        self.output.info("options.shared: {0}; options.fPIC: {1}".format(self.options.shared, self.options.fPIC))
        self.output.info("os: {0}; compiler: {1}; build_type: {2}".format(self.settings.os, self.settings.compiler, self.settings.build_type))
        cmake.configure(source_dir="sources")
        cmake.build()

    def configure(self):
        self.options["gflags"].shared = self.options.shared

    def package(self):
        with tools.chdir("sources"):
            self.copy(pattern="COPYING")
            self.copy("log_severity.h", dst="include/glog", src="glog/src/glog")
            self.copy("logging.h", dst="include/glog", src="glog")
            self.copy("raw_logging.h", dst="include/glog", src="glog")
            self.copy("stl_logging.h", dst="include/glog", src="glog")
            self.copy("vlog_is_on.h", dst="include/glog", src="glog")
            self.copy(pattern="*.dll", dst="bin", src="", keep_path=False)
            self.copy(pattern="*.lib", dst="lib", src="", keep_path=False)
            self.copy(pattern="*.a", dst="lib", src="", keep_path=False)
            self.copy(pattern="*.so*", dst="lib", src="", keep_path=False)
            self.copy(pattern="*.dylib", dst="lib", src="", keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.libs = ["glog"]
            self.cpp_info.libs.extend(['shlwapi'])
        else:
            self.cpp_info.libs = ["glog"]
            self.cpp_info.libs.extend(["pthread"])
