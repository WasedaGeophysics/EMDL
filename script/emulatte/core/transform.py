# Copyright 2021 Waseda Geophysics Laboratory
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-
"""
hankel変換やFD<->TD変換に用いるクラスメソッド

Class List
* HankelTransform
* FourierTransform
"""
import numpy as np
from . import kernels, filters

class HankelTransform:
    """Hankel Transform
    Hankel変換による応答の計算

    Index:
        vmd
        hmdx
        hmdy
        ved
        hedx
        hedy
        circular_loop
        coincident_loop
        grounded_wire
        loop_source
        x_line_source
        y_line_source
    """
    @staticmethod
    def vmd(model, omega):
        """

        """
        y_base, wt0, wt1 = filters.load_hankel_filter(model.hankel_filter)
        model.filter_length = len(y_base)
        model.lambda_ = y_base/model.r
        kernel = kernels.compute_kernel_vmd(model, omega)
        ans = {}
        e_phi = np.dot(wt1, kernel[0]) / model.r
        h_r = np.dot(wt1, kernel[1]) / model.r
        h_z = np.dot(wt0, kernel[2]) / model.r
        ans["e_x"] = -1 / (4 * np.pi) * model.ztilde[model.slayer - 1] \
                        * -model.sin_phi * e_phi
        ans["e_y"] = -1 / (4 * np.pi) * model.ztilde[model.slayer - 1] \
                        *  model.cos_phi * e_phi
        ans["e_z"] = 0
        ans["h_x"] = 1 / (4 * np.pi) * model.cos_phi * h_r
        ans["h_y"] = 1 / (4 * np.pi) * model.sin_phi * h_r
        ans["h_z"] = 1 / (4 * np.pi) * model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1] * h_z 
        return ans

    @staticmethod
    def hmdx(model, omega):
        """

        """
        y_base, wt0, wt1 = filters.load_hankel_filter(model.hankel_filter)
        model.filter_length = len(y_base)
        model.lambda_ = y_base / model.r
        kernel = kernels.compute_kernel_hmd(model, omega)
        ans = {}
        tm_er_1 = np.dot(wt0, kernel[0] * model.lambda_) / model.r
        tm_er_2 = np.dot(wt1, kernel[0]) / model.r
        te_er_1 = np.dot(wt0, kernel[1] * model.lambda_) / model.r
        te_er_2 = np.dot(wt1, kernel[1]) / model.r
        tm_ez = np.dot(wt1, kernel[2] * model.lambda_**2) / model.r
        tm_hr_1 = np.dot(wt0, kernel[3] * model.lambda_) / model.r
        tm_hr_2 = np.dot(wt1, kernel[3]) / model.r
        te_hr_1 = np.dot(wt0, kernel[4] * model.lambda_) / model.r
        te_hr_2 = np.dot(wt1, kernel[4]) / model.r
        te_hz = np.dot(wt1, kernel[5] * model.lambda_**2) / model.r
        amp_tm_ex_1 = -(model.ztilde * model.ytilde)[model.slayer - 1] \
                        * (model.rx - model.sx) * (model.ry - model.sy) \
                        / (4 * np.pi * model.ytilde[model.rlayer - 1] \
                            * model.r ** 2)
        amp_tm_ex_2 =  (model.ztilde * model.ytilde)[model.slayer - 1] \
                        * (model.rx - model.sx) * (model.ry - model.sy) \
                        / (2 * np.pi * model.ytilde[model.rlayer - 1] \
                            * model.r ** 3)
        amp_te_ex_1 = - model.ztilde[model.slayer - 1] \
                        * (model.rx - model.sx) * (model.ry - model.sy) \
                        / (4 * np.pi * model.r ** 2)
        amp_te_ex_2 =   model.ztilde[model.slayer - 1] \
                        * (model.rx - model.sx) * (model.ry - model.sy) \
                        / (2 * np.pi * model.r ** 3)
        amp_tm_ey_1 = -(model.ztilde * model.ytilde)[model.slayer - 1] \
                        * (model.ry - model.sy) ** 2 \
                        / (4 * np.pi * model.ytilde[model.rlayer - 1] \
                            * model.r ** 2)
        amp_tm_ey_2 =  (model.ztilde * model.ytilde)[model.slayer - 1] \
                        / (4 * np.pi * model.ytilde[model.rlayer - 1]) \
                        * (2 * (model.ry - model.sy) ** 2 / model.r ** 3 - 1 \
                            / model.r)
        amp_te_ey_1 =  model.ztilde[model.slayer - 1] \
                        * (model.rx - model.sx) ** 2 \
                        / (4 * np.pi * model.r ** 2)
        amp_te_ey_2 = -model.ztilde[model.slayer - 1] \
                        / (4 * np.pi) * (2 * (model.rx - model.sx) ** 2 \
                            / model.r ** 3 - 1 / model.r)
        amp_tm_ez = - model.ztilde[model.slayer - 1] \
                        * (model.ry - model.sy) / (4 * np.pi * model.r)
        amp_tm_hx_1 = model.k[model.slayer - 1] ** 2  \
                        * (model.ry - model.sy) ** 2 / model.r ** 2 \
                        / (4 * np.pi)
        amp_tm_hx_2 =  - model.k[model.slayer - 1] ** 2 \
                        * (2 * (model.ry - model.sy) ** 2 / model.r ** 3 \
                            - 1 / model.r) / (4 * np.pi)
        amp_te_hx_1 = (model.rx - model.sx) ** 2 / (4 * np.pi * model.r ** 2)\
                        * model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1]
        amp_te_hx_2 = - model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1] \
                        * (2 * (model.rx - model.sx) ** 2 / model.r ** 2 - 1)\
                        / model.r / (4 * np.pi)
        amp_tm_hy_1 = -model.k[model.slayer - 1]** 2 / (4 * np.pi) \
                        * (model.rx - model.sx) * (model.ry - model.sy) \
                        / model.r ** 2
        amp_tm_hy_2 = - amp_tm_hy_1 / model.r * 2
        amp_te_hy_1 = model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1] \
                        / (4 * np.pi) * (model.rx - model.sx) \
                        * (model.ry - model.sy) / model.r ** 2
        amp_te_hy_2 = -model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1] \
                        / (2 * np.pi) * (model.rx - model.sx) \
                        * (model.ry - model.sy) / model.r ** 3
        amp_te_hz = model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1] \
                        * (model.rx - model.sx) / (4 * np.pi * model.r)

        ans["e_x"] = amp_tm_ex_1 * tm_er_1 + amp_tm_ex_2 * tm_er_2 \
                    + amp_te_ex_1 * te_er_1 + amp_te_ex_2 * te_er_2
        ans["e_y"] = amp_tm_ey_1 * tm_er_1 + amp_tm_ey_2 * tm_er_2 \
                    + amp_te_ey_1 * te_er_1 + amp_te_ey_2 * te_er_2
        ans["e_z"] = amp_tm_ez * tm_ez
        ans["h_x"] = amp_tm_hx_1 * tm_hr_1 + amp_tm_hx_2 * tm_hr_2 \
                    + amp_te_hx_1 * te_hr_1 + amp_te_hx_2 * te_hr_2
        ans["h_y"] = amp_tm_hy_1 * tm_hr_1 + amp_tm_hy_2 * tm_hr_2 \
                    + amp_te_hy_1 * te_hr_1 + amp_te_hy_2 * te_hr_2
        ans["h_z"] = amp_te_hz * te_hz
        return ans

    @staticmethod
    def hmdy(model, omega):
        """

        """
        y_base, wt0, wt1 = filters.load_hankel_filter(model.hankel_filter)
        model.filter_length = len(y_base)
        model.lambda_ = y_base / model.r
        kernel = kernels.compute_kernel_hmd(model, omega)
        ans = {}
        tm_er_1 = np.dot(wt0, kernel[0] * model.lambda_) / model.r
        tm_er_2 = np.dot(wt1, kernel[0]) / model.r
        te_er_1 = np.dot(wt0, kernel[1] * model.lambda_) / model.r
        te_er_2 = np.dot(wt1, kernel[1]) / model.r
        tm_ez = np.dot(wt1, kernel[2] * model.lambda_**2) / model.r
        tm_hr_1 = np.dot(wt0, kernel[3] * model.lambda_) / model.r
        tm_hr_2 = np.dot(wt1, kernel[3]) / model.r
        te_hr_1 = np.dot(wt0, kernel[4] * model.lambda_) / model.r
        te_hr_2 = np.dot(wt1, kernel[4]) / model.r
        te_hz = np.dot(wt1, kernel[5]* model.lambda_**2) / model.r

        amp_tm_ex_1 = (model.ztilde * model.ytilde)[model.slayer - 1] \
                        * (model.rx - model.sx) ** 2 \
                        / (4 * np.pi * model.ytilde[model.rlayer - 1] \
                            * model.r ** 2)
        amp_tm_ex_2 = -(model.ztilde * model.ytilde)[model.slayer - 1] \
                        / (4 * np.pi * model.ytilde[model.rlayer - 1]) \
                        * (2 * (model.rx - model.sx) ** 2 / model.r ** 3 \
                            - 1 / model.r)
        amp_te_ex_1 = -model.ztilde[model.slayer - 1] \
                        * (model.ry - model.sy) ** 2 \
                            / (4 * np.pi * model.r ** 2)
        amp_te_ex_2 =  model.ztilde[model.slayer - 1] / (4 * np.pi) \
                        * (2 * (model.ry - model.sy) ** 2 / model.r ** 3 \
                            - 1 / model.r)

        amp_tm_ey_1 = (model.ztilde * model.ytilde)[model.slayer - 1] \
                        * (model.rx - model.sx) * (model.ry - model.sy) \
                        / (4 * np.pi * model.ytilde[model.rlayer - 1] \
                            * model.r ** 2)
        amp_tm_ey_2 = -(model.ztilde * model.ytilde)[model.slayer - 1] \
                        * (model.rx - model.sx) * (model.ry - model.sy) \
                        / (2 * np.pi * model.ytilde[model.rlayer - 1] \
                            * model.r ** 3)
        amp_te_ey_1 = model.ztilde[0,  model.slayer - 1] \
                        * (model.rx - model.sx) * (model.ry - model.sy) \
                        / (4 * np.pi * model.r ** 2)
        amp_te_ey_2 = - model.ztilde[model.slayer - 1] \
                        * (model.rx - model.sx) * (model.ry - model.sy) \
                        / (2 * np.pi * model.r ** 3)
        amp_tm_ez = -(model.ztilde * model.ytilde)[model.slayer - 1] \
                        * (model.rx - model.sx) \
                        / (4 * np.pi * model.ytilde[model.rlayer - 1] \
                            * model.r)

        amp_tm_hx_1 = (model.ztilde * model.ytilde)[model.slayer - 1] \
                        * (model.rx - model.sx) * (model.ry - model.sy) \
                        / (4 * np.pi * model.r ** 2)
        amp_tm_hx_2 = - amp_tm_hx_1 * 2 / model.r
        amp_te_hx_1 = model.ztilde[model.slayer - 1]  \
                        / model.ztilde[model.rlayer - 1] \
                        * (model.rx - model.sx) * (model.ry - model.sy) \
                        / (4 * np.pi * model.r ** 2)
        amp_te_hx_2 = - amp_te_hx_1* 2 / model.r
        amp_tm_hy_1 = -(model.ztilde * model.ytilde)[model.slayer - 1] \
                        * (model.rx - model.sx) ** 2 \
                        / (4 * np.pi * model.r ** 2)
        amp_tm_hy_2 = (model.ztilde * model.ytilde)[model.slayer - 1] \
                        * (2 * (model.rx - model.sx) ** 2 / model.r ** 3 \
                            - 1 / model.r) / (4 * np.pi)
        amp_te_hy_1 = model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1] \
                        * (model.ry - model.sy) ** 2 \
                        / (4 * np.pi * model.r ** 2)
        amp_te_hy_2 = - model.ztilde[0,  model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1] \
                        * (2 * (model.ry - model.sy) ** 2 / model.r ** 3 \
                            - 1 / model.r) / (4 * np.pi)
        amp_te_hz =  model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1] \
                        * (model.ry - model.sy) / (4 * np.pi * model.r)

        ans["e_x"] = amp_tm_ex_1 * tm_er_1 + amp_tm_ex_2 * tm_er_2 \
                        + amp_te_ex_1 * te_er_1 + amp_te_ex_2 * te_er_2
        ans["e_y"] = amp_tm_ey_1 * tm_er_1 + amp_tm_ey_2 * tm_er_2 \
                        + amp_te_ey_1 * te_er_1 + amp_te_ey_2 * te_er_2
        ans["e_z"] = amp_tm_ez * tm_ez
        ans["h_x"] = amp_tm_hx_1 * tm_hr_1 + amp_tm_hx_2 * tm_hr_2 \
                        + amp_te_hx_1 * te_hr_1 + amp_te_hx_2 * te_hr_2
        ans["h_y"] = amp_tm_hy_1 * tm_hr_1 + amp_tm_hy_2 * tm_hr_2 \
                        + amp_te_hy_1 * te_hr_1 + amp_te_hy_2 * te_hr_2
        ans["h_z"] = amp_te_hz * te_hz
        return ans
    
    @staticmethod
    def ved(model, omega):
        """

        """
        y_base, wt0, wt1 = filters.load_hankel_filter(model.hankel_filter)
        model.filter_length = len(y_base)
        model.lambda_ = y_base / model.r
        kernel = kernels.compute_kernel_ved(model, omega)
        ans = {}
        e_phai = np.dot(wt1, kernel[0] * model.lambda_ ** 2) / model.r
        e_z = np.dot(wt0, kernel[1] * model.lambda_ ** 3) / model.r
        h_r = np.dot(wt1, kernel[2] * model.lambda_ ** 2) / model.r

        ans["e_x"] = -1 / (4 * np.pi * model.ytilde[model.rlayer - 1]) \
                    * model.cos_phi * e_phai
        ans["e_y"] = -1 / (4 * np.pi * model.ytilde[model.rlayer - 1]) \
                    * model.sin_phi * e_phai
        ans["e_z"] = 1 / (4 * np.pi * model.ytilde[model.rlayer - 1]) \
                    * e_z
        ans["h_x"] = -1 / (4 * np.pi) * model.sin_phi * h_r
        ans["h_y"] = -1 / (4 * np.pi) * model.cos_phi * h_r
        ans["h_z"] = 0
        return ans
    
    @staticmethod
    def hedx(model, omega):
        """

        """
        y_base, wt0, wt1 = filters.load_hankel_filter(model.hankel_filter)
        model.filter_length = len(y_base)
        model.lambda_ = y_base / model.r
        kernel = kernels.compute_kernel_hed(model, omega)
        ans = {}
        tm_er_1 = np.dot(wt0, kernel[0] * model.lambda_) / model.r
        tm_er_2 = np.dot(wt1, kernel[0]) / model.r
        te_er_1 = np.dot(wt0, kernel[1] * model.lambda_) / model.r
        te_er_2 = np.dot(wt1, kernel[1]) / model.r
        tm_ez = np.dot(wt1, kernel[2] * model.lambda_ ** 2) / model.r
        tm_hr_1 = np.dot(wt0, kernel[3] * model.lambda_) / model.r
        tm_hr_2 = np.dot(wt1, kernel[3]) / model.r
        te_hr_1 = np.dot(wt0, kernel[4] * model.lambda_) / model.r
        te_hr_2 = np.dot(wt1, kernel[4]) / model.r
        te_hz = np.dot(wt1, kernel[5] * model.lambda_**2) / model.r

        amp_tm_ex_g_1 = (model.rx - model.sx) ** 2 \
                        / (4 * np.pi * model.ytilde[model.rlayer - 1] \
                            * model.r ** 2)
        amp_tm_ex_g_2 =  - (2 * (model.rx - model.sx) ** 2 / model.r ** 3 \
                                - 1 / model.r) \
                            / (4 * np.pi \
                                * model.ytilde[model.rlayer - 1])
        amp_te_ex_g_1 = model.ztilde[model.slayer - 1] \
                        * (model.rx - model.sx) ** 2 \
                        / (4 * np.pi * model.r ** 2)
        amp_te_ex_g_2 = - model.ztilde[model.slayer - 1] \
                        * (2 * (model.rx - model.sx) ** 2 / model.r ** 3 \
                            - 1 / model.r) / (4 * np.pi)
        amp_te_ex_line = - model.ztilde[model.slayer - 1] / (4 * np.pi)
        amp_tm_ey_g_1 = (model.rx - model.sx) * (model.ry - model.sy) \
                        / (4 * np.pi * model.ytilde[model.rlayer - 1] \
                            * model.r ** 2)
        amp_tm_ey_g_2 = - (model.rx - model.sx) * (model.ry - model.sy) \
                        / (2 * np.pi * model.ytilde[model.rlayer - 1] \
                            * model.r**3 )
        amp_te_ey_g_1 = + model.ztilde[model.slayer - 1] \
                        * (model.rx - model.sx) * (model.ry - model.sy) \
                        / (4 * np.pi * model.r ** 2)
        amp_te_ey_g_2 = - model.ztilde[model.slayer - 1] \
                        * (model.rx - model.sx) * (model.ry - model.sy) \
                        / (2 * np.pi * model.r ** 3)
        amp_tm_ez = (model.rx - model.sx) \
                        / (4 * np.pi * model.ytilde[model.rlayer - 1] \
                            * model.r)
        amp_tm_hx_g_1 = (model.rx - model.sx) * (model.ry - model.sy) \
                        / (4 * np.pi * model.r ** 2)
        amp_tm_hx_g_2 = - (model.rx - model.sx) * (model.ry - model.sy) \
                        / (2 * np.pi * model.r ** 3)
        amp_te_hx_g_1 = + (model.rx - model.sx) * (model.ry - model.sy) \
                        / (4 * np.pi * model.r ** 2) \
                        * model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1]
        amp_te_hx_g_2 = - (model.rx - model.sx) * (model.ry - model.sy) \
                        / (2 * np.pi * model.r ** 3) \
                        * model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1]
        amp_tm_hy_g_1 = -(model.rx - model.sx) ** 2 \
                        / (4 * np.pi * model.r ** 2)
        amp_tm_hy_g_2 = (2 * (model.rx - model.sx) ** 2 / model.r ** 3 \
                            - 1 / model.r) / (4 * np.pi)
        amp_te_hy_g_1 = - (model.rx - model.sx) ** 2 \
                        / (4 * np.pi * model.r ** 2) \
                        * model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1]
        amp_te_hy_g_2 = (2 * (model.rx - model.sx) ** 2 / model.r ** 3 \
                        - 1 / model.r) / (4 * np.pi) \
                        * model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1]
        amp_te_hy_line = model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1] \
                        / (4 * np.pi)
        amp_te_hz_line = model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1] \
                        * (model.ry - model.sy) / (4 * np.pi * model.r)

        ans["e_x"] = amp_tm_ex_g_1 * tm_er_1 + amp_tm_ex_g_2 * tm_er_2 \
                        + amp_te_ex_g_1 * te_er_1 + amp_te_ex_g_2 * te_er_2 \
                        + amp_te_ex_line * te_er_1
        ans["e_y"] = amp_tm_ey_g_1 * tm_er_1 + amp_tm_ey_g_2 * tm_er_2 \
                        + amp_te_ey_g_1 * te_er_1 + amp_te_ey_g_2 * te_er_2
        ans["e_z"] = amp_tm_ez * tm_ez
        ans["h_x"] = amp_tm_hx_g_1 * tm_hr_1 + amp_tm_hx_g_2 * tm_hr_2 \
                        + amp_te_hx_g_1 * te_hr_1 + amp_te_hx_g_2 * te_hr_2
        ans["h_y"] = amp_tm_hy_g_1 * tm_hr_1 + amp_tm_hy_g_2 * tm_hr_2 \
                        + amp_te_hy_g_1 * te_hr_1 + amp_te_hy_g_2 * te_hr_2 \
                        + amp_te_hy_line * te_hr_1
        ans["h_z"] = amp_te_hz_line * te_hz
        return ans
    
    @staticmethod
    def hedy(model, omega):
        """

        """
        y_base, wt0, wt1 = filters.load_hankel_filter(model.hankel_filter)
        model.filter_length = len(y_base)
        model.lambda_ = y_base / model.r
        kernel = kernels.compute_kernel_hed(model, omega)
        ans = {}
        tm_er_1 = np.dot(wt0, kernel[0] * model.lambda_) / model.r
        tm_er_2 = np.dot(wt1, kernel[0]) / model.r
        te_er_1 = np.dot(wt0, kernel[1] * model.lambda_) / model.r
        te_er_2 = np.dot(wt1, kernel[1]) / model.r
        tm_ez = np.dot(wt1, kernel[2] * model.lambda_**2) / model.r
        tm_hr_1 = np.dot(wt0, kernel[3] * model.lambda_) / model.r
        tm_hr_2 = np.dot(wt1, kernel[3]) / model.r
        te_hr_1 = np.dot(wt0, kernel[4] * model.lambda_) / model.r
        te_hr_2 = np.dot(wt1, kernel[4]) / model.r
        te_hz = np.dot(wt1, kernel[5] * model.lambda_**2) / model.r

        amp_tm_ex_g_1 = (model.rx - model.sx) * (model.ry - model.sy) \
                        / (4 * np.pi * model.ytilde[model.rlayer - 1] \
                            * model.r ** 2)
        amp_tm_ex_g_2 = - (model.rx - model.sx) * (model.ry - model.sy) \
                        / (2 * np.pi * model.ytilde[model.rlayer - 1] \
                            * model.r ** 3)
        amp_te_ex_g_1 = model.ztilde[model.slayer - 1] \
                        * (model.rx - model.sx) * (model.ry - model.sy) \
                        / (4 * np.pi * model.r ** 2)
        amp_te_ex_g_2 = - model.ztilde[model.slayer - 1] \
                        * (model.rx - model.sx) * (model.ry - model.sy) \
                        / (2 * np.pi * model.r ** 3)
        amp_tm_ey_g_1 = (model.ry - model.sy) ** 2 \
                        / (4 * np.pi * model.ytilde[model.rlayer - 1] \
                            * model.r ** 2)
        amp_tm_ey_g_2 = - (2 * (model.ry - model.sy) ** 2 / model.r ** 3 \
                            - 1 / model.r) \
                        / (4 * np.pi* model.ytilde[model.rlayer - 1])
        amp_te_ey_g_1 =  model.ztilde[model.slayer - 1] \
                        * (model.ry - model.sy) ** 2 \
                        / (4 * np.pi * model.r ** 2)
        amp_te_ey_g_2 = -model.ztilde[model.slayer - 1] \
                        * (2 * (model.ry - model.sy) ** 2 / model.r ** 3 \
                            - 1 / model.r) / (4 * np.pi)
        amp_te_ey_line = - model.ztilde[model.slayer - 1] / (4 * np.pi)
        amp_tm_ez = (model.ry - model.sy) / (4 * np.pi \
                        * model.ytilde[model.rlayer - 1] * model.r)
        amp_tm_hx_g_1 = (model.ry - model.sy) ** 2 \
                        / (4 * np.pi * model.r ** 2)
        amp_tm_hx_g_2 = - (2 * (model.ry - model.sy) ** 2 / model.r ** 3 \
                            - 1 / model.r) / (4 * np.pi)
        amp_te_hx_g_1 = + (model.ry - model.sy) ** 2 \
                        / (4 * np.pi * model.r ** 2) \
                        * model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1]
        amp_te_hx_g_2 = - (2 * (model.ry - model.sy) ** 2 / model.r ** 3 \
                        - 1 / model.r) / (4 * np.pi) \
                        * model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1]
        amp_te_hx_line = -model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1] / (4 * np.pi)
        amp_tm_hy_g_1 = - (model.rx - model.sx) * (model.ry - model.sy) \
                        / (4 * np.pi * model.r ** 2)
        amp_tm_hy_g_2 = (model.rx - model.sx) * (model.ry - model.sy) \
                        / (2 * np.pi * model.r ** 3)
        amp_te_hy_g_1 = - (model.rx - model.sx) * (model.ry - model.sy) \
                        / (4 * np.pi * model.r ** 2) \
                        * model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1]
        amp_te_hy_g_2 = (model.rx - model.sx) * (model.ry - model.sy) \
                        / (2 * np.pi * model.r ** 3) \
                        * model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1]
        amp_te_hz_line = -model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1] \
                        * (model.rx - model.sx) / (4 * np.pi * model.r)

        ans["e_x"] = amp_tm_ex_g_1 * tm_er_1 + amp_tm_ex_g_2 * tm_er_2 \
                        + amp_te_ex_g_1 * te_er_1 + amp_te_ex_g_2 * te_er_2
        ans["e_y"] = amp_tm_ey_g_1 * tm_er_1 + amp_tm_ey_g_2 * tm_er_2 \
                        + amp_te_ey_g_1 * te_er_1 + amp_te_ey_g_2 * te_er_2 \
                        + amp_te_ey_line * te_er_1
        ans["e_z"] = amp_tm_ez * tm_ez
        ans["h_x"] = amp_tm_hx_g_1 * tm_hr_1 + amp_tm_hx_g_2 * tm_hr_2 \
                        + amp_te_hx_g_1 * te_hr_1 + amp_te_hx_g_2 * te_hr_2 \
                        + amp_te_hx_line * te_hr_1
        ans["h_y"] = amp_tm_hy_g_1 * tm_hr_1 + amp_tm_hy_g_2 * tm_hr_2 \
                        + amp_te_hy_g_1 * te_hr_1 + amp_te_hy_g_2 * te_hr_2
        ans["h_z"] = amp_te_hz_line * te_hz
        return ans
    
    @staticmethod
    def circular_loop(model, omega):
        """

        """
        y_base, wt0, wt1 = filters.load_hankel_filter(model.hankel_filter)
        model.filter_length = len(y_base)
        model.lambda_ = y_base / model.src.radius
        kernel = kernels.compute_kernel_circular(model, omega)
        ans = {}
        e_phai = np.dot(wt1, kernel[0]) / model.src.radius
        h_r = np.dot(wt1, kernel[1]) / model.src.radius
        h_z = np.dot(wt1, kernel[2]) / model.src.radius
        ans["e_x"] =  model.ztilde[model.slayer - 1] * model.src.radius\
                        * model.sin_phi / 2 * e_phai
        ans["e_y"] = -model.ztilde[model.slayer - 1] * model.src.radius\
                        * model.cos_phi / 2 * e_phai
        ans["e_z"] = 0
        ans["h_x"] = -model.src.radius * model.ztilde[model.slayer - 1]\
                        / model.ztilde[model.rlayer - 1] \
                        * model.cos_phi / 2 * h_r
        ans["h_y"] = -model.src.radius * model.ztilde[model.slayer - 1]\
                        / model.ztilde[model.rlayer - 1] \
                        * model.sin_phi / 2 * h_r
        ans["h_z"] = model.src.radius * model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1] / 2 * h_z
        return ans
    
    @staticmethod
    def coincident_loop(model, omega):
        """

        """
        y_base, wt0, wt1 = filters.load_hankel_filter(model.hankel_filter)
        model.filter_length = len(y_base)
        model.lambda_ = y_base / model.r
        kernel = kernels.compute_kernel_coincident(model, omega)
        ans = {}
        h_z_co = np.dot(wt1, kernel[0]) / model.src.radius
        ans["e_x"] = 0
        ans["e_y"] = 0
        ans["e_z"] = 0
        ans["h_x"] = 0
        ans["h_y"] = 0
        ans["h_z"] = (1 * np.pi * model.src.radius ** 2 * h_z_co)
        return ans
    
    @staticmethod
    def grounded_wire(model, omega):
        """

        """
        y_base, wt0, wt1 = filters.load_hankel_filter(model.hankel_filter)
        model.filter_length = len(y_base)
        y_base_wire = np.ones((model.filter_length, model.src.nsplit)) \
                        * np.array([y_base]).T
        lambda_ = y_base_wire / model.rn
        kernel = np.zeros((6, model.filter_length, model.src.nsplit), dtype=complex)
        for i in range(model.src.nsplit):
            model.lambda_ = lambda_[:,i]
            kernel[:,:,i] = kernels.compute_kernel_hed(model, omega)
        model.lambda_ = lambda_
        tm_er_g_first = np.dot(wt1, kernel[0][:, 0]) / model.rn[0]
        tm_er_g_end = np.dot(wt1, kernel[0][:, model.src.nsplit - 1]) \
                        / model.rn[model.src.nsplit - 1]
        te_er_g_first = np.dot(wt1, kernel[1][:, 0]) / model.rn[0]
        te_er_g_end = np.dot(wt1, kernel[1][:, model.src.nsplit - 1]) \
                        / model.rn[model.src.nsplit - 1]
        tm_ez_1 = np.dot(wt0, kernel[2][:, 0] * model.lambda_[:, 0]) \
                        / model.rn[0]
        tm_ez_2 = np.dot(wt0, kernel[2][:, model.src.nsplit - 1] \
                        * model.lambda_[:, model.src.nsplit - 1]) \
                        / model.rn[model.src.nsplit - 1]
        tm_hr_g_first = np.dot(wt1, kernel[3][:, 0]) / model.rn[0]
        tm_hr_g_end = np.dot(wt1, kernel[3][:, model.src.nsplit - 1]) \
                        / model.rn[model.src.nsplit - 1]
        te_hr_g_first = np.dot(wt1, kernel[4][:, 0]) / model.rn[0]
        te_hr_g_end = np.dot(wt1, kernel[4][:, model.src.nsplit - 1]) \
                        / model.rn[model.src.nsplit - 1]
        te_hz_l = np.dot(wt1, kernel[5] * model.lambda_ ** 2) / model.rn
        te_ex_l = np.dot(wt0, kernel[1] * model.lambda_) / model.rn
        te_hy_l = np.dot(wt0, kernel[4] * model.lambda_) / model.rn

        amp_tm_ex_1 = (model.xx[0] / model.rn[0]) \
                        / (4 * np.pi * model.ytilde[model.rlayer - 1])
        amp_tm_ex_2 = (-model.xx[model.src.nsplit-1] \
                            / model.rn[model.src.nsplit-1]) \
                        / (4 * np.pi * model.ytilde[model.rlayer - 1])
        amp_te_ex_1 = (model.xx[0] / model.rn[0]) \
                        * model.ztilde[model.slayer - 1] / (4 * np.pi)
        amp_te_ex_2 = (-model.xx[model.src.nsplit-1] \
                        / model.rn[model.src.nsplit-1]) \
                        * model.ztilde[model.slayer - 1] / (4 * np.pi)
        te_ex_line = -model.ztilde[model.slayer - 1] / (4 * np.pi)
        amp_tm_ey_1 = (model.yy[0] / model.rn[0]) \
                        / (4 * np.pi * model.ytilde[model.rlayer - 1])
        amp_tm_ey_2 = (-model.yy[model.src.nsplit-1] \
                        / model.rn[model.src.nsplit-1]) \
                        / (4 * np.pi * model.ytilde[model.rlayer - 1])
        amp_te_ey_1 = (model.yy[0] / model.rn[0]) \
                        * model.ztilde[model.slayer - 1] / (4 * np.pi)
        amp_te_ey_2 =  (-model.yy[model.src.nsplit-1] \
                        / model.rn[model.src.nsplit-1]) \
                        * model.ztilde[model.slayer - 1] / (4 * np.pi)
        amp_tm_ez_1 = 1 / (4 * np.pi * model.ytilde[model.rlayer - 1])
        amp_tm_ez_2 = -1 / (4 * np.pi * model.ytilde[model.rlayer - 1])
        amp_tm_hx_1 = 1 / (4 * np.pi) * model.yy[0] / model.rn[0]
        amp_tm_hx_2 = - 1 / (4 *np.pi) * model.yy[model.src.nsplit-1] \
                        / model.rn[model.src.nsplit-1]
        amp_te_hx_1 = model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1] / (4 * np.pi) \
                        * model.yy[0] / model.rn[0]
        amp_te_hx_2 = - model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1] / (4 *np.pi) \
                        * model.yy[model.src.nsplit-1] \
                        / model.rn[model.src.nsplit-1]
        amp_tm_hy_1 = -1 / (4 * np.pi) * model.xx[0] / model.rn[0]
        amp_tm_hy_2 = 1 / ( 4 *np.pi) * model.xx[model.src.nsplit-1] \
                        / model.rn[model.src.nsplit-1]
        amp_te_hy_1 = -model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1] / (4 * np.pi) \
                        * model.xx[0] / model.rn[0]
        amp_te_hy_2 = model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1] / (4 * np.pi) \
                        * model.xx[model.src.nsplit-1] \
                        / model.rn[model.src.nsplit-1]
        te_hy_line = model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1] / (4 * np.pi)

        rot_ans = {}
        rot_ans["e_x"] = (amp_tm_ex_1 * tm_er_g_first \
                        + amp_tm_ex_2 * tm_er_g_end \
                        + amp_te_ex_1 * te_er_g_first \
                        + amp_te_ex_2 * te_er_g_end) \
                        + te_ex_line * model.ds \
                        * np.dot(te_ex_l, np.ones((model.src.nsplit)))
        rot_ans["e_y"] = amp_tm_ey_1 * tm_er_g_first + amp_tm_ey_2 * tm_er_g_end \
                        + amp_te_ey_1 * te_er_g_first \
                        + amp_te_ey_2 * te_er_g_end
        rot_ans["e_z"] = amp_tm_ez_1 * tm_ez_1 + amp_tm_ez_2 * tm_ez_2
        rot_ans["h_x"] = (amp_tm_hx_1 * tm_hr_g_first \
                        + amp_tm_hx_2 * tm_hr_g_end \
                        + amp_te_hx_1 * te_hr_g_first \
                        + amp_te_hx_2 * te_hr_g_end)
        rot_ans["h_y"] = amp_tm_hy_1 * tm_hr_g_first \
                        + amp_tm_hy_2 * tm_hr_g_end \
                        + amp_te_hy_1 * te_hr_g_first \
                        + amp_te_hy_2 * te_hr_g_end \
                        + te_hy_line * model.ds \
                        * np.dot(te_hy_l, np.ones((model.src.nsplit)))
        rot_ans["h_z"] = np.dot(model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1] \
                        * model.yy / model.rn * model.ds / (4*np.pi) \
                        ,te_hz_l.T)
        ans = {}
        ans["e_x"] = model.cos_theta * rot_ans["e_x"] - model.sin_theta * rot_ans["e_y"]
        ans["e_y"] = model.cos_theta * rot_ans["e_y"] + model.sin_theta * rot_ans["e_x"]
        ans["e_z"] = rot_ans["e_z"]
        ans["h_x"] = model.cos_theta * rot_ans["h_x"] - model.sin_theta * rot_ans["h_y"]
        ans["h_y"] = model.cos_theta * rot_ans["h_y"] + model.sin_theta * rot_ans["h_x"]
        ans["h_z"] = rot_ans["h_z"]
        return ans
    
    @staticmethod
    def loop_source(model, omega):
        """

        """
        y_base, wt0, wt1 = filters.load_hankel_filter(model.hankel_filter)
        model.filter_length = len(y_base)
        model.lambda_ = y_base / model.r
        kernel = kernels.compute_kernel_hed(model, omega)
        ans = {}
        te_ex_l = np.dot(wt0, kernel[1] * model.lambda_) / model.rn
        te_hy_l = np.dot(wt0, kernel[4] * model.lambda_) / model.rn
        te_hz_l = np.dot(wt1, kernel[5] * model.lambda_ ** 2) / model.rn
        te_ex_line = -model.ztilde[model.slayer - 1] / (4 * np.pi)
        te_hy_line = model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1] / (4 * np.pi)

        ans["e_x"] =  te_ex_line * model.ds \
                        * np.dot(te_ex_l, np.ones((model.src.num_dipole,1)))
        ans["e_y"] = 0
        ans["e_z"] = 0
        ans["h_x"] = 0
        ans["h_y"] = te_hy_line * model.ds \
                        * np.dot(te_hy_l, np.ones((model.src.num_dipole,1)))
        ans["h_z"] = np.dot(model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1] \
                        * model.yy / model.rn * model.ds / (4*np.pi) \
                        , te_hz_l.T)
        return ans

    @staticmethod
    def x_line_source(model, omega):
        """

        """
        y_base, wt0, wt1 = filters.load_hankel_filter(model.hankel_filter)
        model.filter_length = len(y_base)
        model.lambda_ = y_base / model.r
        kernel = kernels.compute_kernel_hed(model, omega)
        ans = {}
        te_er_1 = np.dot(wt0, kernel[1] * model.lambda_) / model.r
        te_hr_1 = np.dot(wt0, kernel[4] * model.lambda_) / model.r
        te_hz = np.dot(wt1, kernel[5] * model.lambda_**2) / model.r

        amp_te_ex_line = - model.ztilde[model.slayer - 1] / (4 * np.pi)
        amp_te_hy_line = model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1] / (4 * np.pi)
        amp_te_hz_line = model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1] \
                        * (model.ry - model.sy) / (4 * np.pi * model.r)

        ans["e_x"] = model.ds * amp_te_ex_line * te_er_1
        ans["e_y"] = 0
        ans["e_z"] = 0
        ans["h_x"] = 0
        ans["h_y"] = model.ds * amp_te_hy_line * te_hr_1
        ans["h_z"] = model.ds * amp_te_hz_line * te_hz
        return ans

    @staticmethod
    def y_line_source(model, omega):
        """

        """
        y_base, wt0, wt1 = filters.load_hankel_filter(model.hankel_filter)
        model.filter_length = len(y_base)
        model.lambda_ = y_base / model.r
        kernel = kernels.compute_kernel_hed(model, omega)
        ans = {}
        te_er_1 = np.dot(wt0, kernel[1] * model.lambda_) / model.r
        te_hr_1 = np.dot(wt0, kernel[4] * model.lambda_) / model.r
        te_hz = np.dot(wt1, kernel[5] * model.lambda_ ** 2) / model.r

        amp_te_ey_line = - model.ztilde[model.slayer - 1] / (4 * np.pi)
        amp_te_hx_line = -model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1] / (4 * np.pi)
        amp_te_hz_line = - model.ztilde[model.slayer - 1] \
                        / model.ztilde[model.rlayer - 1] \
                        * (model.rx - model.sx) / (4 * np.pi * model.r)
        ans["e_x"] = 0
        ans["e_y"] = model.ds * amp_te_ey_line * te_er_1
        ans["e_z"] = 0
        ans["h_x"] = model.ds * amp_te_hx_line * te_hr_1
        ans["h_y"] = 0
        ans["h_z"] = model.ds * amp_te_hz_line * te_hz
        return ans

class FourierTransform:
    @staticmethod
    def euler_transform(model, time):
        """
        フーリエ変換のデジタルフィルタでオイラーのフィルタを用いた変換。
        時間微分でないものは後々実装予定。
        """
        ans = {}
        y_base_time, wt0_time, wt1_time = filters.load_fft_filter(
                                            'raito_time_250')
        filter_length_time = len(y_base_time)
        e_x_set = np.zeros((filter_length_time, 1), dtype=complex)
        e_y_set = np.zeros((filter_length_time, 1), dtype=complex)
        e_z_set = np.zeros((filter_length_time, 1), dtype=complex)
        h_x_set = np.zeros((filter_length_time, 1), dtype=complex)
        h_y_set = np.zeros((filter_length_time, 1), dtype=complex)
        h_z_set = np.zeros((filter_length_time, 1), dtype=complex)
        time_range = time - model.src.freqtime[0]
        omega_set = y_base_time / time_range
        for ii in range(filter_length_time):
            omega = omega_set[ii]
            hankel_result = model.src.hankel_transform(model, omega)
            e_x_set[ii] = hankel_result["e_x"]
            e_y_set[ii] = hankel_result["e_y"]
            e_z_set[ii] = hankel_result["e_z"]
            h_x_set[ii] = hankel_result["h_x"]
            h_y_set[ii] = hankel_result["h_y"]
            h_z_set[ii] = hankel_result["h_z"]

        ans["e_x"] = -np.dot(wt1_time.T, np.imag(e_x_set)) \
                        * (2.0 * time_range / np.pi) ** 0.5 / time_range
        ans["e_y"] = -np.dot(wt1_time.T, np.imag(e_y_set)) \
                        * (2.0 * time_range / np.pi) ** 0.5 / time_range
        ans["e_z"] = -np.dot(wt1_time.T, np.imag(e_z_set)) \
                        * (2.0 * time_range / np.pi) ** 0.5 / time_range
        ans["h_x"] = -np.dot(wt1_time.T, np.imag(h_x_set)) \
                        * (2.0 * time_range / np.pi) ** 0.5 / time_range
        ans["h_y"] = -np.dot(wt1_time.T, np.imag(h_y_set)) \
                        * (2.0 * time_range / np.pi) ** 0.5 / time_range
        ans["h_z"] = -np.dot(wt1_time.T, np.imag(h_z_set)) \
                        * (2.0 * time_range / np.pi) ** 0.5 / time_range
        return ans

    @staticmethod
    def fast_fourier_transform(model, f, time, time_diff):
        """
        フーリエ正弦・余弦変換による周波数→時間領域への変換。
        (ただし、三次spline補間により計算時間を高速化)
        f :  -
            spline補間により得られた周波数領域における電磁応答の多項式近似
        """
        base, cos, sin = filters.load_fft_filter(
                            'anderson_sin_cos_filter_787')

        if not time_diff:
            omega_base = base / time
            f = f(omega_base)
            f_imag =  -2 / np.pi * np.imag(f) / omega_base
            ans = np.dot(f_imag, cos.T) / time
        else:
            omega_base = base / time
            f = f(omega_base)
            f_imag = 2 / np.pi * np.imag(f)
            ans = np.dot(f_imag, sin.T) / time
        return ans

    # TODO DLAG ！コードに無駄が多いので要修正　修正完了まで非推奨とする

    @staticmethod
    def dlagf0em(model, nb, emfield):
        abscis = 0.7866057737580476e0
        e = 1.10517091807564762e0
        er = .904837418035959573e0
        nofun = 0
        base, cos, sin = filters.load_fft_filter(
                        'anderson_sin_cos_filter_787')
        ffl = len(base)
        bmax = model.src.freqtime[-1]
        tol = 1e-12
        ntol = 1
        key = np.zeros(ffl)
        dwork = np.zeros(ffl)
        dans = np.zeros(nb)
        arg = np.zeros(nb)

        if (nb < 1 or bmax <= 0.0e0):
            raise Exception('TimeRangeError: End of time is too early.')

        y = bmax * er ** (np.fix(nb) - 1)
        if (y <= 0.0e0):
            raise Exception('TimeRangeError: End of time is too early.')

        i = ffl + 1
        nb1 = np.fix(nb) + 1
        y1 = abscis / bmax
        lag = -1

        for ilag in range(1, nb+1):
            lag += 1
            istore = np.int(nb1 - ilag)
            if lag > 0:
                y1 *= e
            arg[istore-1] = abscis / y1
            none = 0
            itol = np.fix(ntol)
            dsum = 0.0e0
            cmax = 0.0e0

            y = y1
            m = 20
            i = 426
            y *= e
            look = i + lag
            iq = look / (ffl + 1)
            ir = look % (ffl + 1)
            if (ir == 0):
                ir = 1
            iroll = iq * ffl
            if (key[ir-1] <= iroll):
                key[ir-1] = iroll + ir
                g = y

                hankel_result = model.src.hankel_transform(model, g) 
                dwork[ir-1] = np.imag(hankel_result[emfield]) / g
                nofun = np.fix(np.fix(nofun) + 1)

            c = dwork[ir-1] * cos[i-1]
            dsum = dsum + c
            goon = 1

            while (m != 0):
                while (goon == 1):
                    if (m == 20):
                        cmax = np.max([abs(c), cmax])
                        i = i + 1
                        y = y * e
                        if (i <= 461):
                            break
                        if (cmax == 0.0e0):
                            none = 1
                        cmax = tol * cmax
                        m = 30
                        break
                    if (m == 30):
                        if (~(abs(c) <= cmax)):
                            itol = np.fix(ntol)
                            i = i + 1
                            y = y * e
                            if (i <= ffl):
                                break
                        itol = itol - 1
                        goon1 = 1
                        while (itol > 0 and i < ffl):
                            i = i + 1
                            y = y * e
                            if (i <= ffl):
                                goon1 = 0
                                break
                            itol = itol - 1
                        if (goon1 == 0):
                            break
                        itol = np.fix(ntol)
                        y = y1
                        m = 60
                        i = 425
                        break
                    if (m == 60):
                        if (~(abs(c) <= cmax and none == 0)): # ???
                            itol = np.fix(ntol)
                            i = i - 1
                            y = y * er
                            if (i > 0):
                                break
                        itol = itol - 1
                        goon1 = 1
                        while (itol > 0 and i > 1):
                            i = i - 1
                            y = y * er
                            if (i > 0):
                                goon1 = 0
                                break
                            itol = itol - 1
                        if (goon1 == 0):
                            break
                        goon = 0
                        m = 0
                if (goon!=0):
                    look = i + ilag
                    iq = look / (ffl+1)
                    ir = look % (ffl+1)
                    if (ir == 0):
                        ir = 1
                    iroll = iq * 787
                    if (key[ir-1] <= iroll):
                        key[ir-1] = iroll + ir
                        g = y
                        hankel_result = model.src.hankel_transform(model, g)
                        dwork[ir-1] = np.imag(hankel_result[emfield]) / g
                        nofun = np.fix(np.fix(nofun) + 1)
                    c = dwork[ir-1] * cos[i-1]
                    dsum = dsum + c
            dans[istore-1] = dsum
            continue
        return dans, arg

    @staticmethod
    def dlagf1em(model, nb, emfield):
        abscis = 0.7745022656977834e0
        e = 1.10517091807564762e0
        er = .904837418035959573e0
        nofun = 0
        base, cos, sin = filters.load_fft_filter(
                            'anderson_sin_cos_filter_787')
        ffl = len(base)
        bmax = model.src.freqtime[-1]
        tol = 1e-12
        ntol = 1
        key = np.zeros((ffl))
        dwork = np.zeros((ffl))
        dans = np.zeros(nb)
        arg = np.zeros(nb)

        if (nb < 1 or bmax <= 0.0e0):
            raise Exception('TimeRangeError: End of time is too early.')

        y = bmax * er ** (np.fix(nb) - 1)
        if (y <= 0.0e0):
            raise Exception('TimeRangeError: End of time is too early.')

        ierr = 0
        i = ffl + 1
        nb1 = np.fix(nb) + 1
        y1 = abscis / bmax
        lag = -1

        for ilag in range (1, nb + 1):
            lag += 1
            istore = np.int(nb - ilag)
            if lag > 0:
                y1 *= e
            arg[istore-1] = abscis / y1
            none = 0
            itol = np.fix(ntol)
            dsum = 0.0e0
            cmax = 0.0e0
            y = y1
            m = 20
            i = 426
            y = y * e
            look = i + lag
            iq = look / (ffl + 1)
            ir = look % (ffl + 1)
            if (ir == 0):
                ir = 1
            iroll = iq * ffl
            if (key[ir-1] <= iroll):
                key[ir-1] = iroll + ir
                g = y
                hankel_result = model.src.hankel_transform(model, g)
                dwork[ir-1] = np.imag(hankel_result[emfield])
                nofun = np.fix(np.fix(nofun) + 1)

            c = dwork[ir-1] * sin[i-1]
            dsum = dsum + c
            goon = 1


            while (m != 0):
                while (goon == 1):
                    if (m == 20):
                        cmax = np.max([abs(c), cmax])
                        i = i + 1
                        y = y * e
                        if (i <= 463):
                            break
                        if (cmax == 0.0e0):
                            none = 1
                        cmax = tol * cmax
                        m = 30
                        break
                    if (m == 30):
                        if (~(abs(c) <= cmax)):
                            itol = np.fix(ntol)
                            i = i + 1
                            y = y * e
                            if (i <= 787):
                                break
                        itol = itol - 1
                        goon1 = 1
                        while (itol > 0 and i < 787):
                            i = i + 1
                            y = y * e
                            if (i <= 787):
                                goon1 = 0
                                break
                            itol = itol - 1
                        if (goon1 == 0):
                            break
                        itol = np.fix(ntol)
                        y = y1
                        m = 60
                        i = 425
                        break
                    if (m == 60):
                        if (~(abs(c) <= cmax and none == 0)):
                            itol = np.fix(ntol)
                            i = i - 1
                            y = y * er
                            if (i > 0):
                                break
                        itol = itol - 1
                        goon1 = 1
                        while itol > 0 and i > 1:
                            i = i - 1
                            y = y * er
                            if i > 0:
                                goon1 = 0
                                break
                            itol = itol - 1
                        if goon1 == 0:
                            break
                        goon = 0
                        m = 0
                if goon != 0:
                    look = i + ilag
                    iq = look / (ffl + 1)
                    ir = look % (ffl + 1)
                    if ir == 0:
                        ir = 1
                    iroll = iq * 787
                    if key[ir-1] <= iroll:
                        key[ir-1] = iroll + ir
                        g = y
                        hankel_result = model.src.hankel_transform(model, g)
                        dwork[ir-1] = np.imag(hankel_result[emfield])
                        nofun = np.fix(np.fix(nofun) + 1)
                    c = dwork[ir-1] * sin[i-1]
                    dsum = dsum + c
            dans[istore-1] = dsum
            continue
        return dans, arg
