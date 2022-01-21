#!/bin/bash

set -e

print_usage_and_exit() {
  echo "Usage: $0 cpu|cuda [spec_file] [population_size] [problem_size] [generations]"
  echo ""
  echo "Compiles and runs the given .ez algorithm specification with the given"
  echo "parameters. Problem size is available as \$PROBLEM_SIZE in the algorithm code."
  echo ""
  echo "Example: $0 cpu one_max.ez 100 100 100"
  exit 1
}

if [ $# -ne 5 ]; then
  print_usage_and_exit
fi

mode="$1"
spec_path="$2"
population_size="$3"
problem_size="$4"
generations="$5"

# Install EASEA into a local directory

root_dir="$(realpath "$(dirname "$0")")"

cd "$root_dir"

build_dir="$root_dir/build"

repo_dir="$build_dir/easea"
install_dir="$build_dir/install"
easea_dir="$install_dir/usr/local/easena"

mkdir -p "$build_dir"

if [ ! -d "$repo_dir" ]; then
  git clone https://github.com/EASEA/easea.git "$repo_dir"
fi

if [ ! -d "$install_dir" ]; then
  mkdir "$install_dir"
  cd "$repo_dir"
  cmake .
  make
  make DESTDIR="$install_dir" install
  cd "$root_dir"
fi

# Compile and run the given algorithm

run_dir="$build_dir/run"

rm -rf "$run_dir"
mkdir "$run_dir"

cp "$spec_path" "$run_dir/spec.ez"

sed -i -e "s/\$PROBLEM_SIZE/$problem_size/g" "$run_dir/spec.ez"

cd "$run_dir"

if [ "$mode" == "cuda" ]; then
  easea_flags="-cuda"
fi

EZ_PATH="$easea_dir/" PATH="$PATH:$easea_dir/bin" easena spec.ez $easea_flags
EZ_PATH="$easea_dir/" CPLUS_INCLUDE_PATH="$easea_dir/libeasea/include/" make

"$run_dir/spec" --popSize $population_size --nbOffspring $population_size --nbGen $generations
