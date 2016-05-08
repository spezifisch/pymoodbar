# This file is part of pymoodbar.
# Copyright 2016, szf <spezifisch@users.noreply.github.com>
#
# pymoodbar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pymoodbar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pymoodbar.  If not, see <http://www.gnu.org/licenses/>.

cmake_minimum_required(VERSION 2.6)

# for Qt stuff
set(CMAKE_AUTOMOC ON)
set(CMAKE_INCLUDE_CURRENT_DIR ON)

# it rocks
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

# boost::python
find_package(Boost 1.55.0 REQUIRED COMPONENTS python)

# python
INCLUDE_DIRECTORIES("${Boost_INCLUDE_DIRS}" "/usr/include/python2.7")

# qt
find_package(Qt4 4.4.3 REQUIRED QtGui)

# output to parent dir
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "../")
# source files
ADD_LIBRARY(pymoodbar SHARED MoodbarInterface.cpp moodbarbuilder.cpp moodbarrenderer.cpp)
# no "lib" at beginning of .so filename
SET_TARGET_PROPERTIES(pymoodbar PROPERTIES PREFIX "" )
TARGET_LINK_LIBRARIES(pymoodbar ${Boost_LIBRARIES} Qt4::QtGui)
