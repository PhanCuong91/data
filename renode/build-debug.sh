# myprofile: describes all the needed tool for our application
export CONAN_PROFILE=./myprofile

# Installing all the tool that were in the myprofile 
conan install ./conan -if ./build/conan --profile $CONAN_PROFILE

# Extracting all the bin folders of needed tools
python -u ./conan/conan_path.py

# Temporary adding these paths to PATH environemnt variable
source ./build/conan/shell_path.sh

echo $PATH
mkdir build
cd build && cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Debug -D "CMAKE_TOOLCHAIN_FILE=../CMake/GNU-ARM-Toolchain.cmake" ../
make
cd ./../
renode ./renode-config_test.resc

