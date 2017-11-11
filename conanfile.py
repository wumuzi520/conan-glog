from conans import ConanFile, CMake, tools


class GlogConan(ConanFile):
    name = "glog"
    version = "0.3.5"
    license = "MIT"
    url = "https://github.com/DariuszOstolski/conan-glog.git"
    description = "C++ implementation of the Google logging module"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    requires = "gflags/v2.2.1@dostolski/testing"

    def source(self):
        self.run("git clone https://github.com/google/glog.git")
        self.run("cd glog && git checkout -b v0.3.5-conan v0.3.5")
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("glog/CMakeLists.txt", "include (DetermineGflagsNamespace)", '''include (DetermineGflagsNamespace)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        self.run('cmake glog %s' % cmake.command_line)
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("log_severity.h", dst="include/glog", src="glog/src/glog")
        self.copy("logging.h", dst="include/glog", src="glog")
        self.copy("raw_logging.h", dst="include/glog", src="glog")
        self.copy("stl_logging.h", dst="include/glog", src="glog")
        self.copy("vlog_is_on.h", dst="include/glog", src="glog")
        self.copy("*glog.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["glog"]
