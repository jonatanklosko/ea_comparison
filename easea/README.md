# EASEA

The `run.sh` script automates compilation of EASEA and individual `.ez`
files, both for the CPU and GPU.

## Environment setup

To ensure successful compilation you need to make sure the necessary
dependencies are in place.

### System dependencies

EASEA expects a number of system dependencies to be installed,
for Debian/Ubuntu you can use the following:

```
sudo apt-get -y install flex bison valgrind gzip unzip wget cmake
```

For more details see [Installing EASEA](http://easea.unistra.fr/index.php/Installing_EASEA).

### GCC version

EASEA doesn't compile under GCC 11+, due to missing `<limits>` headers.
Starting GCC 11 those headers need to be included explicitly
([reference](https://www.gnu.org/software/gcc/gcc-11/porting_to.html#header-dep-changes)).

If you use a more recent version of GCC, make sure to include the headers:

```
# Make sure the version in the path matches your GCC version
export CXXFLAGS="-include /usr/include/c++/11/limits"
```

or use an older GCC version altogether:

```
export CXX=g++-9
```
