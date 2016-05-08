/* This file is part of pymoodbar.
   Copyright 2016, szf <spezifisch@users.noreply.github.com>

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

#include "moodbarbuilder.h"
#include "moodbarrenderer.h"

#include <boost/python.hpp>

#include <QPalette>

#include <string>

using namespace boost::python;

boost::python::list Render(boost::python::list &data, int width, int height, std::string outfile) {
    std::vector<char> svdata = to_std_vector<char>(data);
    QByteArray qdata(svdata.data(), svdata.size());
    ColorVector colors = MoodbarRenderer::Colors(qdata, MoodbarRenderer::Style_Normal, QPalette());
    QImage img = MoodbarRenderer::RenderToImage(colors, QSize(width, height));

    if (outfile != "") {
        img.save(outfile.c_str());
    }

    const unsigned char *imgbits = img.bits();
    boost::python::list ret;
    for (int i = 0; i < img.width()*img.height(); i++) {
        ret.append(imgbits[i]);
    }
    return ret;
}

BOOST_PYTHON_MODULE(pymoodbar)
{
    class_<MoodbarBuilder>("MoodbarBuilder", init<>())
        .def("Init", &MoodbarBuilder::Init)
        .def("AddFrame", &MoodbarBuilder::AddFramePy)
        .def("Finish", &MoodbarBuilder::FinishPy)
    ;

    def("Render", &Render);
}
