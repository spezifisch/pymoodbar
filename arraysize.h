/* This file is part of pymoodbar.
   Based on code from Clementine:
   Copyright 2014, David Sansome <me@davidsansome.com>

   pymoodbar is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   pymoodbar is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with pymoodbar.  If not, see <http://www.gnu.org/licenses/>.
*/

template <typename T>
constexpr size_t arraysize(const T&) {
  static_assert(std::is_array<T>::value, "Argument must be array");
  return std::extent<T>::value;
}
