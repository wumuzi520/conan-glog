#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class GlogConan(ConanFile):
    name = "glog"
    version = "0.3.5"
    url = "https://github.com/bincrafters/conan-glog"
    description = "Google logging library"
    license = "BSD 3-Clause"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt", "FindGLog.cmake"]
    source_subfolder = "source_subfolder"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False], "with_gflags": [True, False], "with_threads": [True, False]}
    default_options = "shared=False", "fPIC=True", "with_gflags=True", "with_threads=True"

    def configure(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

        if self.options.with_gflags:
            self.requires("gflags/2.2.1@ant/stable")
        

    def source(self):
        source_url =  "https://github.com/google/{0}".format(self.name)
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def build(self):
        cmake = CMake(self)
        cmake.definitions['WITH_GFLAGS'] = self.options.with_gflags
        cmake.definitions['WITH_THREADS'] = self.options.with_threads
        cmake.definitions['BUILD_TESTING'] = False
        if self.settings.os != "Windows":
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("FindGLog.cmake", ".", ".")
        self.copy("COPYING", dst="licenses", src=self.source_subfolder)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
