# -*- coding: utf-8

"""Module for components of type turbomachinery.

Components in this module:

    - :func:`tespy.components.turbomachinery.turbomachine` (parent class)
    - :func:`tespy.components.turbomachinery.compressor`
    - :func:`tespy.components.turbomachinery.pump`
    - :func:`tespy.components.turbomachinery.turbine`


This file is part of project TESPy (github.com/oemof/tespy). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location tespy/components/turbomachinery.py

SPDX-License-Identifier: MIT
"""

import logging

import numpy as np

from tespy.components.components import component
from tespy.tools.characteristics import load_default_char as ldc
from tespy.tools.characteristics import compressor_map

from tespy.tools.data_containers import dc_cc, dc_cp, dc_cm, dc_simple
from tespy.tools.fluid_properties import (
        h_ps, s_ph, T_mix_ph, h_mix_ps, s_mix_ph, s_mix_pT, v_mix_ph,
        num_fluids, err)
from tespy.tools.helpers import TESPyComponentError

# %%


class turbomachine(component):
    r"""
    The component turbomachine is the parent class for pump, compressor and
    turbine.

    Equations

        **mandatory equations**

        - :func:`tespy.components.components.component.fluid_func`
        - :func:`tespy.components.components.component.mass_flow_func`

        **optional equations**

        .. math::

            0 = \dot{m}_{in} \cdot \left( h_{out} - h_{in} \right) - P\\
            0 = pr \cdot p_{in} - p_{out}

        isentropic efficiency equations (optional)

        - :func:`tespy.components.turbomachinery.pump.eta_s_func`
        - :func:`tespy.components.turbomachinery.compressor.eta_s_func`
        - :func:`tespy.components.turbomachinery.turbine.eta_s_func`

        **additional equations**

        - :func:`tespy.components.turbomachinery.pump.additional_equations`
        - :func:`tespy.components.turbomachinery.compressor.additional_equations`
        - :func:`tespy.components.turbomachinery.turbine.additional_equations`

    Inlets/Outlets

        - in1
        - out1

    Parameters
    ----------
    label : str
        The label of the component.

    design : list
        List containing design parameters (stated as String).

    offdesign : list
        List containing offdesign parameters (stated as String).

    P : String/float/tespy.helpers.dc_cp
        Power, :math:`P/\text{W}`

    eta_s : String/float/tespy.helpers.dc_cp
        Isentropic efficiency, :math:`\eta_s/1`

    pr : String/float/tespy.helpers.dc_cp
        Outlet to inlet pressure ratio, :math:`pr/1`

    eta_s_char : str/tespy.helpers.dc_cc
        Characteristic curve for isentropic efficiency, provide x and y values
        or use generic values (e. g. calculated from design case).

    Example
    -------
    For an example please refer to:

    - :class:`tespy.components.turbomachinery.compressor`
    - :class:`tespy.components.turbomachinery.pump`
    - :class:`tespy.components.turbomachinery.turbine`
    """

    @staticmethod
    def component():
        return 'turbomachine'

    @staticmethod
    def attr():
        return {'P': dc_cp(), 'eta_s': dc_cp(), 'pr': dc_cp(),
                'eta_s_char': dc_cc(), 'Sirr': dc_simple()}

    @staticmethod
    def inlets():
        return ['in1']

    @staticmethod
    def outlets():
        return ['out1']

    def comp_init(self, nw):

        component.comp_init(self, nw)

        if ((nw.mode == 'offdesign' or self.local_offdesign is True) and
                self.local_design is False):
            self.dh_s_ref = (self.h_os('pre') - self.inl[0].h.design)

        self.fl_deriv = self.fluid_deriv()
        self.m_deriv = self.mass_flow_deriv()

    def equations(self):
        r"""
        Calculates vector vec_res with results of equations for this component.

        Returns
        -------
        vec_res : list
            Vector of residual values.
        """

        vec_res = []

        ######################################################################
        # eqations for fluids
        vec_res += self.fluid_func()

        ######################################################################
        # eqations for mass flow balance
        vec_res += self.mass_flow_func()

        ######################################################################
        # eqations for specified power
        if self.P.is_set:
            vec_res += [self.inl[0].m.val_SI * (
                    self.outl[0].h.val_SI - self.inl[0].h.val_SI) - self.P.val]

        ######################################################################
        # eqations for specified pressure ratio
        if self.pr.is_set:
            vec_res += [self.pr.val * self.inl[0].p.val_SI -
                        self.outl[0].p.val_SI]

        ######################################################################
        # eqations for specified isentropic efficiency
        if self.eta_s.is_set:
            self.eta_s_res = self.eta_s_func()
            vec_res += [self.eta_s_res]

        ######################################################################
        # additional equations
        vec_res += self.additional_equations()

        return vec_res

    def additional_equations(self):
        r"""
        Calculates vector vec_res with results of additional equations for this
        component.

        Returns
        -------
        vec_res : list
            Vector of residual values.
        """
        return []

    def derivatives(self):
        r"""
        Calculates matrix of partial derivatives for given equations.

        Returns
        -------
        mat_deriv : ndarray
            Matrix of partial derivatives.
        """
        mat_deriv = []

        ######################################################################
        # derivatives fluid composition
        mat_deriv += self.fl_deriv

        ######################################################################
        # derivatives for mass flow balance
        mat_deriv += self.m_deriv

        ######################################################################
        # derivatives for specified power
        if self.P.is_set:
            P_deriv = np.zeros((1, 2 + self.num_vars, self.num_fl + 3))
            P_deriv[0, 0, 0] = self.outl[0].h.val_SI - self.inl[0].h.val_SI
            P_deriv[0, 0, 2] = -self.inl[0].m.val_SI
            P_deriv[0, 1, 2] = self.inl[0].m.val_SI
            mat_deriv += P_deriv.tolist()

        ######################################################################
        # derivatives for specified pressure ratio
        if self.pr.is_set:
            pr_deriv = np.zeros((1, 2 + self.num_vars, self.num_fl + 3))
            pr_deriv[0, 0, 1] = self.pr.val
            pr_deriv[0, 1, 1] = -1
            mat_deriv += pr_deriv.tolist()

        ######################################################################
        # derivatives for specified isentropic efficiency
        if self.eta_s.is_set:
            mat_deriv += self.eta_s_deriv()

        ######################################################################
        # derivatives for additional equations
        mat_deriv += self.additional_derivatives()

        return np.asarray(mat_deriv)

    def additional_derivatives(self):
        r"""
        Calculates matrix of partial derivatives for given additional
        equations.

        Returns
        -------
        mat_deriv : ndarray
            Matrix of partial derivatives.
        """
        return []

    def eta_s_func(self):
        r"""
        Calculates residual value of isentropic efficiency function, see
        subclasses.
        """
        msg = ('If you want to use eta_s as parameter, please specify which '
               'type of turbomachine you are using.')
        logging.error(msg)
        raise TESPyComponentError(msg)

    def eta_s_deriv(self):
        r"""
        Calculates partial derivatives for isentropic efficiency function, see
        subclasses.
        """
        msg = ('If you want to use eta_s as parameter, please specify which '
               'type of turbomachine you are using.')
        logging.error(msg)
        raise TESPyComponentError(msg)

    def h_os(self, mode):
        r"""
        Calculates the enthalpy at the outlet if compression or expansion is
        isentropic.

        Parameters
        ----------
        mode : str
            Determines wheather calculation is in preprocessing mode.

        Returns
        -------
        h : float
            Enthalpy after isentropic state change.

            .. math::

                h = \begin{cases}
                h\left(p_{out}, s\left(p_{in}, h_{in}\right) \right) &
                \text{pure fluids}\\
                h\left(p_{out}, s\left(p_{in}, T_{in}\right) \right) &
                \text{mixtures}\\
                \end{cases}
        """
        if mode == 'pre':
            i = self.inl[0].to_flow_design()
            o = self.outl[0].to_flow_design()
        else:
            i = self.inl[0].to_flow()
            o = self.outl[0].to_flow()

        if num_fluids(i[3]) == 1:
            for fluid, x in i[3].items():
                if x > err:
                    return h_ps(o[1], s_ph(i[1], i[2], fluid), fluid)
        else:
            T_mix = T_mix_ph(i, T0=self.inl[0].T.val_SI)
            s_mix = s_mix_pT(i, T_mix)
            return h_mix_ps(o, s_mix, T0=self.outl[0].T.val_SI)

    def bus_func(self, bus):
        r"""
        Calculates the residual value of the bus function.

        Parameters
        ----------
        bus : tespy.connections.bus
            TESPy bus object.

        Returns
        -------
        val : float
            Residual value of equation.

            .. math::

                P = \dot{m}_{in} \cdot \left( h_{out} - h_{in} \right)\\
                val = P \cdot f_{char}\left( \frac{P}{P_{ref}}\right)
        """
        i = self.inl[0].to_flow()
        o = self.outl[0].to_flow()
        val = i[0] * (o[2] - i[2])
        if np.isnan(bus.P_ref):
            expr = 1
        else:
            expr = abs(val / bus.P_ref)
        return val * bus.char.evaluate(expr)

    def bus_deriv(self, bus):
        r"""
        Calculates the matrix of partial derivatives of the bus function.

        Parameters
        ----------
        bus : tespy.connections.bus
            TESPy bus object.

        Returns
        -------
        mat_deriv : ndarray
            Matrix of partial derivatives.
        """
        deriv = np.zeros((1, 2, len(self.inl[0].fluid.val) + 3))
        deriv[0, 0, 0] = self.numeric_deriv(self.bus_func, 'm', 0, bus=bus)
        deriv[0, 0, 2] = self.numeric_deriv(self.bus_func, 'h', 0, bus=bus)
        deriv[0, 1, 2] = self.numeric_deriv(self.bus_func, 'h', 1, bus=bus)
        return deriv

    def calc_parameters(self):
        r"""
        Postprocessing parameter calculation.
        """
        i, o = self.inl[0].to_flow(), self.outl[0].to_flow()
        self.P.val = i[0] * (o[2] - i[2])
        self.pr.val = o[1] / i[1]
        self.Sirr.val = self.inl[0].m.val_SI * (
                s_mix_ph(self.outl[0].to_flow()) -
                s_mix_ph(self.inl[0].to_flow()))

# %%


class compressor(turbomachine):
    r"""
    Equations

        **mandatory equations**

        - :func:`tespy.components.components.component.fluid_func`
        - :func:`tespy.components.components.component.mass_flow_func`

        **optional equations**

        .. math::

            0 = \dot{m}_{in} \cdot \left( h_{out} - h_{in} \right) - P\\
            0 = pr \cdot p_{in} - p_{out}

        - :func:`tespy.components.turbomachinery.compressor.eta_s_func`

        **additional equations**

        - :func:`tespy.components.turbomachinery.compressor.additional_equations`

    Inlets/Outlets

        - in1
        - out1

    Image

        .. image:: _images/compressor.svg
           :scale: 100 %
           :alt: alternative text
           :align: center

    Parameters
    ----------
    label : str
        The label of the component.

    design : list
        List containing design parameters (stated as String).

    offdesign : list
        List containing offdesign parameters (stated as String).

    P : String/float/tespy.helpers.dc_cp
        Power, :math:`P/\text{W}`

    eta_s : String/float/tespy.helpers.dc_cp
        Isentropic efficiency, :math:`\eta_s/1`

    pr : String/float/tespy.helpers.dc_cp
        Outlet to inlet pressure ratio, :math:`pr/1`

    eta_s_char : str/tespy.helpers.dc_cc
        Characteristic curve for isentropic efficiency, provide x and y values
        or use generic values (e. g. calculated from design case).

    char_map : str/tespy.helpers.dc_cm
        Characteristic map for pressure rise and isentropic efficiency vs.
        nondimensional mass flow, see
        tespy.components.characteristics.compressor for further information.

    igva : str/float/tespy.helpers.dc_cp
        Inlet guide vane angle, :math:`igva/^\circ`.

    Example
    -------
    Create an air compressor model and calculate the power required for
    compression of 50 l/s of ambient air to 5 bars. Using a generic compressor
    map how does the efficiency change in different operation mode (e. g. 90 %
    of nominal volumetric flow)?

    >>> from tespy.components import sink, source, compressor
    >>> from tespy.connections import connection
    >>> from tespy.networks import network
    >>> import shutil
    >>> fluid_list = ['air']
    >>> nw = network(fluids=fluid_list, p_unit='bar', T_unit='C',
    ... h_unit='kJ / kg', v_unit='l / s', iterinfo=False)
    >>> si = sink('sink')
    >>> so = source('source')
    >>> comp = compressor('compressor')
    >>> comp.component()
    'compressor'
    >>> inc = connection(so, 'out1', comp, 'in1')
    >>> outg = connection(comp, 'out1', si, 'in1')
    >>> nw.add_conns(inc, outg)

    Specify the compressor parameters: nominal efficiency and pressure ratio.
    For offdesign mode the characteristic map is selected instead of the
    isentropic efficiency. For offdesign, the inlet guide vane angle should be
    variable in order to maintain the same pressure ratio at a different
    volumetric flow.

    >>> comp.set_attr(pr=5, eta_s=0.8, design=['eta_s'],
    ... offdesign=['char_map'])
    >>> inc.set_attr(fluid={'air': 1}, p=1, T=20, v=50)
    >>> nw.solve('design')
    >>> nw.save('tmp')
    >>> round(comp.P.val, 0)
    12772.0
    >>> inc.set_attr(v=45)
    >>> comp.set_attr(igva='var')
    >>> nw.solve('offdesign', design_path='tmp')
    >>> round(comp.eta_s.val, 2)
    0.77
    >>> shutil.rmtree('./tmp', ignore_errors=True)
    """

    @staticmethod
    def component():
        return 'compressor'

    @staticmethod
    def attr():
        return {'P': dc_cp(min_val=0),
                'eta_s': dc_cp(min_val=0, max_val=1),
                'pr': dc_cp(min_val=1),
                'igva': dc_cp(min_val=-45, max_val=45, d=1e-2, val=0),
                'char_map': dc_cm(),
                'eta_s_char': dc_cc(param='m'),
                'Sirr': dc_simple()}

    def comp_init(self, nw):

        component.comp_init(self, nw)

        if self.char_map.func is None:
            self.char_map.func = ldc(
                self.component(), 'char_map', 'DEFAULT', compressor_map)

            if self.char_warnings is True:
                msg = ('Created characteristic map for parameter char_map '
                       ' at component ' + self.label + ' from default data.\n'
                       'You can specify your own data using component.char_map'
                       '.set_attr(func=custom_char).\n'
                       'If you want to disable these warnings use '
                       'component.char_warnings=False.')
                logging.warning(msg)

        self.fl_deriv = self.fluid_deriv()
        self.m_deriv = self.mass_flow_deriv()

    def additional_equations(self):
        r"""
        Calculates vector vec_res with results of additional equations for
        compressor.

        Equations

            **optional equations**

            - :func:`tespy.components.turbomachinery.compressor.eta_s_char_func`
            - :func:`tespy.components.turbomachinery.compressor.char_map_func`

        Returns
        -------
        vec_res : list
            Vector of residual values.
        """
        vec_res = []

        ######################################################################
        # equations for specified characteristic map
        if self.char_map.is_set:
            vec_res += self.char_map_func().tolist()

        ######################################################################
        # equation for specified isentropic efficiency characteristics
        if self.eta_s_char.is_set:
            vec_res += [self.eta_s_char_func()]

        return vec_res

    def additional_derivatives(self):
        r"""
        Calculates matrix of partial derivatives for given additional
        equations.

        Returns
        -------
        mat_deriv : list
            Matrix of partial derivatives.
        """
        mat_deriv = []

        ######################################################################
        # derivatives for specified characteristic map
        if self.char_map.is_set:
            mat_deriv += self.char_map_deriv()

        ######################################################################
        # derivatives for specified isentropic efficiency characteristics
        if self.eta_s_char.is_set:
            mat_deriv += self.eta_s_char_deriv()

        return mat_deriv

    def eta_s_func(self):
        r"""
        Equation for given isentropic efficiency of a compressor.

        Returns
        -------
        res : float
            Residual value of equation.

            .. math::

                0 = -\left( h_{out} - h_{in} \right) \cdot \eta_{s,c} +
                \left( h_{out,s} - h_{in} \right)
        """
        return (-(self.outl[0].h.val_SI - self.inl[0].h.val_SI) *
                self.eta_s.val + (self.h_os('post') - self.inl[0].h.val_SI))

    def eta_s_deriv(self):
        r"""
        Calculates the matrix of partial derivatives of the isentropic
        efficiency function.

        Returns
        -------
        deriv : list
            Matrix of partial derivatives.
        """
        mat_deriv = np.zeros((1, 2 + self.num_vars, self.num_fl + 3))

        mat_deriv[0, 0, 1] = self.numeric_deriv(self.eta_s_func, 'p', 0)
        mat_deriv[0, 1, 1] = self.numeric_deriv(self.eta_s_func, 'p', 1)
        mat_deriv[0, 0, 2] = self.numeric_deriv(self.eta_s_func, 'h', 0)
        mat_deriv[0, 1, 2] = -self.eta_s.val

        return mat_deriv.tolist()

    def eta_s_char_func(self):
        r"""
        Equation for given isentropic efficiency characteristic of a
        compressor.

        Returns
        -------
        res : ndarray
            Residual value of equation.

            .. math::

                0 = \left( h_{out} - h_{in} \right) \cdot
                \frac{\Delta h_{s,ref}}{\Delta h_{ref}}
                \cdot char\left( \dot{m}_{in} \cdot v_{in} \right) -
                \left( h_{out,s} - h_{in} \right)
        """
        # actual values
        i = self.inl[0].to_flow()
        o = self.outl[0].to_flow()
        # design values
        i_d = self.inl[0].to_flow_design()
        o_d = self.outl[0].to_flow_design()

        expr = 1
        if self.eta_s_char.param == 'm':
            if not np.isnan(i_d[0]):
                expr = i[0] / i_d[0]
        elif self.eta_s_char.param == 'pr':
            if not np.isnan([i_d[1], o_d[1]]).any():
                expr = (o[1] * i_d[1]) / (i[1] * o_d[1])
        else:
            msg = ('Must provide a parameter for eta_s_char at component ' +
                   self.label + '.')
            logging.error(msg)
            raise ValueError(msg)

        return (self.eta_s.design * self.eta_s_char.func.evaluate(expr) *
                (o[2] - i[2]) - (self.h_os('post') - i[2]))

    def eta_s_char_deriv(self):
        r"""
        Calculates the matrix of partial derivatives of the isentropic
        efficiency characteristic function.

        Returns
        -------
        deriv : list
            Matrix of partial derivatives.
        """
        mat_deriv = np.zeros((1, 2 + self.num_vars, self.num_fl + 3))

        mat_deriv[0, 0, 1] = self.numeric_deriv(self.eta_s_char_func, 'p', 0)
        mat_deriv[0, 1, 1] = self.numeric_deriv(self.eta_s_char_func, 'p', 1)
        mat_deriv[0, 0, 2] = self.numeric_deriv(self.eta_s_char_func, 'h', 0)
        mat_deriv[0, 1, 2] = self.numeric_deriv(self.eta_s_char_func, 'h', 1)

        return mat_deriv.tolist()

    def char_map_func(self):
        r"""
        Equations for characteristic map of compressor.

        Parameters

            - X: speedline index (rotational speed is constant)
            - Y: nondimensional mass flow
            - Z1: pressure ratio equation
            - Z2: isentropic efficiency equation
            - igva: variable inlet guide vane angle (assumed 0° if not
              specified)

            .. math::

                X = \sqrt{\frac{T_\mathrm{1,ref}}{T_\mathrm{1}}}

                Y = \frac{\dot{m}_\mathrm{1} \cdot p_\mathrm{1,ref}}
                {\dot{m}_\mathrm{1,ref} \cdot p_\mathrm{1} \cdot X}

                Z1 = \frac{p_2 \cdot p_\mathrm{1,ref}}
                {p_1 \cdot p_\mathrm{2,ref}}-
                pr_{c}(char(m, igva))

                Z2 = \frac{\eta_\mathrm{s,c}}{\eta_\mathrm{s,c,ref}} -
                \eta_{s,c}(char(m, igva))

        Returns
        -------
        res : ndarray (Z1, Z2)
            Residual values of equations.
        """
        # actual values
        i = self.inl[0].to_flow()
        o = self.outl[0].to_flow()
        # design values
        i_d = self.inl[0].to_flow_design()
        o_d = self.outl[0].to_flow_design()

        T_i = T_mix_ph(i, T0=self.inl[0].T.val_SI)

        x = np.sqrt(T_mix_ph(i_d) / T_i)
        y = (i[0] * i_d[1]) / (i_d[0] * i[1] * x)

        pr, eta = self.char_map.func.evaluate(x, y, self.igva.val)

        z1 = o[1] * i_d[1] / (i[1] * o_d[1]) - pr
        z2 = ((self.h_os('post') - i[2]) / (o[2] - i[2]) /
              self.eta_s.design - eta)

        return np.array([z1, z2])

    def char_map_deriv(self):
        r"""
        Calculates the matrix of partial derivatives of the compressor
        characteristic map function.

        Returns
        -------
        deriv : list
            Matrix of partial derivatives.
        """
        m11 = self.numeric_deriv(self.char_map_func, 'm', 0)
        p11 = self.numeric_deriv(self.char_map_func, 'p', 0)
        h11 = self.numeric_deriv(self.char_map_func, 'h', 0)

        p21 = self.numeric_deriv(self.char_map_func, 'p', 1)
        h21 = self.numeric_deriv(self.char_map_func, 'h', 1)

        if self.igva.is_var:
            igva = self.numeric_deriv(self.char_map_func, 'igva', 1)

        deriv = np.zeros((2, 2 + self.num_vars, self.num_fl + 3))
        deriv[0, 0, 0] = m11[0]
        deriv[0, 0, 1] = p11[0]
        deriv[0, 0, 2] = h11[0]
        deriv[0, 1, 1] = p21[0]
        deriv[0, 1, 2] = h21[0]
        deriv[1, 0, 0] = m11[1]
        deriv[1, 0, 1] = p11[1]
        deriv[1, 0, 2] = h11[1]
        deriv[1, 1, 1] = p21[1]
        deriv[1, 1, 2] = h21[1]
        if self.igva.is_var:
            deriv[0, 2 + self.igva.var_pos, 0] = igva[0]
            deriv[1, 2 + self.igva.var_pos, 0] = igva[1]
        return deriv.tolist()

    def convergence_check(self, nw):
        r"""
        Performs a convergence check.

        Parameters
        ----------
        nw : tespy.networks.network
            The network object using this component.

        Note
        ----
        Manipulate enthalpies/pressure at inlet and outlet if not specified by
        user to match physically feasible constraints.
        """
        i, o = self.inl, self.outl

        if o[0].init_csv is False:
            if not o[0].p.val_set and o[0].p.val_SI < i[0].p.val_SI:
                o[0].p.val_SI = o[0].p.val_SI * 2

            if not o[0].h.val_set and o[0].h.val_SI < i[0].h.val_SI:
                o[0].h.val_SI = o[0].h.val_SI * 1.1

        if i[0].init_csv is False:
            if not i[0].p.val_set and o[0].p.val_SI < i[0].p.val_SI:
                i[0].p.val_SI = o[0].p.val_SI * 0.5
            if not i[0].h.val_set and o[0].h.val_SI < i[0].h.val_SI:
                i[0].h.val_SI = o[0].h.val_SI * 0.9

    @staticmethod
    def initialise_source(c, key):
        r"""
        Returns a starting value for pressure and enthalpy at component's
        outlet.

        Parameters
        ----------
        c : tespy.connections.connection
            Connection to perform initialisation on.

        key : str
            Fluid property to retrieve.

        Returns
        -------
        val : float
            Starting value for pressure/enthalpy in SI units.

            .. math::

                val = \begin{cases}
                10^6 & \text{key = 'p'}\\
                6 \cdot 10^5 & \text{key = 'h'}
                \end{cases}
        """
        if key == 'p':
            return 10e5
        elif key == 'h':
            return 6e5

    @staticmethod
    def initialise_target(c, key):
        r"""
        Returns a starting value for pressure and enthalpy at component's
        inlet.

        Parameters
        ----------
        c : tespy.connections.connection
            Connection to perform initialisation on.

        key : str
            Fluid property to retrieve.

        Returns
        -------
        val : float
            Starting value for pressure/enthalpy in SI units.

            .. math::

                val = \begin{cases}
                10^5 & \text{key = 'p'}\\
                4 \cdot 10^5 & \text{key = 'h'}
                \end{cases}
        """
        if key == 'p':
            return 1e5
        elif key == 'h':
            return 4e5

    def calc_parameters(self):
        r"""
        Postprocessing parameter calculation.
        """
        turbomachine.calc_parameters(self)

        self.eta_s.val = ((self.h_os('post') - self.inl[0].h.val_SI) /
                          (self.outl[0].h.val_SI - self.inl[0].h.val_SI))

        if self.char_map.is_set:
            # get bound errors for characteristic map
            i = self.inl[0].to_flow()
            i_d = self.inl[0].to_flow_design()
            T_i = T_mix_ph(i, T0=self.inl[0].T.val_SI)
            x = np.sqrt(T_mix_ph(i_d)) / np.sqrt(T_i)
            y = (i[0] * i_d[1]) / (i_d[0] * i[1] * x)
            self.char_map.func.get_bound_errors(x, y, self.igva.val,
                                                self.label)

        if self.eta_s_char.is_set:
            # get bound errors for isentropic efficiency characteristics
            i = self.inl[0].to_flow()
            o = self.outl[0].to_flow()
            i_d = self.inl[0].to_flow_design()
            o_d = self.outl[0].to_flow_design()

            expr = 1
            if self.eta_s_char.param == 'm':
                if not np.isnan(i_d[0]):
                    expr = i[0] / i_d[0]
            elif self.eta_s_char.param == 'pr':
                if not np.isnan([i_d[1], o_d[1]]).any():
                    expr = (o[1] * i_d[1]) / (i[1] * o_d[1])

            self.eta_s_char.func.get_bound_errors(expr, self.label)

        self.check_parameter_bounds()

# %%


class pump(turbomachine):
    r"""
    Equations

        **mandatory equations**

        - :func:`tespy.components.components.component.fluid_func`
        - :func:`tespy.components.components.component.mass_flow_func`

        **optional equations**

        .. math::

            0 = \dot{m}_{in} \cdot \left( h_{out} - h_{in} \right) - P\\
            0 = pr \cdot p_{in} - p_{out}

        - :func:`tespy.components.turbomachinery.pump.eta_s_func`

        **additional equations**

        - :func:`tespy.components.turbomachinery.pump.additional_equations`

    Inlets/Outlets

        - in1
        - out1

    Image

        .. image:: _images/pump.svg
           :scale: 100 %
           :alt: alternative text
           :align: center

    Parameters
    ----------
    label : str
        The label of the component.

    design : list
        List containing design parameters (stated as String).

    offdesign : list
        List containing offdesign parameters (stated as String).

    P : String/float/tespy.helpers.dc_cp
        Power, :math:`P/\text{W}`

    eta_s : String/float/tespy.helpers.dc_cp
        Isentropic efficiency, :math:`\eta_s/1`

    pr : String/float/tespy.helpers.dc_cp
        Outlet to inlet pressure ratio, :math:`pr/1`

    eta_s_char : str/tespy.helpers.dc_cc
        Characteristic curve for isentropic efficiency, provide x and y values
        or use generic values (e. g. calculated from design case).

    flow_char : str/tespy.helpers.dc_cc
        Characteristic curve for pressure rise vs. volumetric flow rate,
        provide data: :math:`x/\frac{\text{m}^3}{\text{s}} \,
        y/\text{Pa}`

    Example
    -------
    A pump with a known pump curve (difference pressure as function of
    volumetric flow) pumps 1,5 l/s of water in design conditions. E. g. for a
    given isentropic efficiency it is possible to calculate power consumption
    and pressure at the pump.

    >>> from tespy.components import sink, source, pump
    >>> from tespy.connections import connection
    >>> from tespy.networks import network
    >>> from tespy.tools.characteristics import char_line
    >>> from tespy.tools.data_containers import dc_cc
    >>> import shutil
    >>> fluid_list = ['water']
    >>> nw = network(fluids=fluid_list, p_unit='bar', T_unit='C',
    ...     h_unit='kJ / kg', v_unit='l / s', iterinfo=False)
    >>> si = sink('sink')
    >>> so = source('source')
    >>> pu = pump('pump')
    >>> pu.component()
    'pump'
    >>> inc = connection(so, 'out1', pu, 'in1')
    >>> outg = connection(pu, 'out1', si, 'in1')
    >>> nw.add_conns(inc, outg)

    After that we calculate offdesign performance using
    the pump curve and a characteristic function for the pump efficiency. We
    can calulate the offdesign efficiency and the volumetric flow, if the
    difference pressure changed.
    TODO: Link to deufalt characteristic lines?

    >>> v = np.array([0, 0.4, 0.8, 1.2, 1.6, 2]) / 1000
    >>> dp = np.array([15, 14, 12, 9, 5, 0]) * 1e5
    >>> char = char_line(x=v, y=dp)
    >>> pu.set_attr(eta_s=0.8, flow_char=dc_cc(func=char, is_set=True),
    ... design=['eta_s'], offdesign=['eta_s_char'])
    >>> inc.set_attr(fluid={'water': 1}, p=1, T=20, v=1.5, design=['v'])
    >>> nw.solve('design')
    >>> nw.save('tmp')
    >>> round(pu.pr.val, 0)
    7.0
    >>> round(outg.p.val - inc.p.val, 0)
    6.0
    >>> round(pu.P.val, 0)
    1125.0
    >>> outg.set_attr(p=12)
    >>> nw.solve('offdesign', design_path='tmp')
    >>> round(pu.eta_s.val, 2)
    0.71
    >>> round(inc.v.val, 1)
    0.9
    >>> shutil.rmtree('./tmp', ignore_errors=True)
    """

    @staticmethod
    def component():
        return 'pump'

    @staticmethod
    def attr():
        return {'P': dc_cp(min_val=0),
                'eta_s': dc_cp(min_val=0, max_val=1),
                'pr': dc_cp(min_val=1),
                'eta_s_char': dc_cc(),
                'flow_char': dc_cc(),
                'Sirr': dc_simple()}

    def additional_equations(self):
        r"""
        Calculates vector vec_res with results of additional equations for
        pump.

        Equations

            **optional equations**

            - :func:`tespy.components.turbomachinery.pump.eta_s_char_func`
            - :func:`tespy.components.turbomachinery.pump.flow_char_func`

        Returns
        -------
        vec_res : list
            Vector of residual values.
        """
        vec_res = []

        ######################################################################
        # equations for specified isentropic efficiency characteristics
        if self.eta_s_char.is_set:
            vec_res += [self.eta_s_char_func()]

        ######################################################################
        # equations for specified pressure rise vs. flowrate characteristics
        if self.flow_char.is_set:
            vec_res += [self.flow_char_func()]

        return vec_res

    def additional_derivatives(self):
        r"""
        Calculates matrix of partial derivatives for given additional
        equations.

        Returns
        -------
        mat_deriv : list
            Matrix of partial derivatives.
        """
        mat_deriv = []

        ######################################################################
        # derivatives for specified isentropic efficiency characteristics
        if self.eta_s_char.is_set:
            mat_deriv += self.eta_s_char_deriv()

        ######################################################################
        # derivatives for specified pressure rise vs. flowrate characteristics
        if self.flow_char.is_set:
            mat_deriv += self.flow_char_deriv()

        return mat_deriv

    def eta_s_func(self):
        r"""
        Equation for given isentropic efficiency of a pump.

        Returns
        -------
        res : float
            Residual value of equation.

            .. math::

                0 = -\left( h_{out} - h_{in} \right) \cdot \eta_{s,c} +
                \left( h_{out,s} - h_{in} \right)
        """
        return (-(self.outl[0].h.val_SI - self.inl[0].h.val_SI) *
                self.eta_s.val + (self.h_os('post') - self.inl[0].h.val_SI))

    def eta_s_deriv(self):
        r"""
        Calculates the matrix of partial derivatives of the isentropic
        efficiency function.

        Returns
        -------
        deriv : list
            Matrix of partial derivatives.
        """
        deriv = np.zeros((1, 2 + self.num_vars, self.num_fl + 3))

        deriv[0, 0, 1] = self.numeric_deriv(self.eta_s_func, 'p', 0)
        deriv[0, 1, 1] = self.numeric_deriv(self.eta_s_func, 'p', 1)
        deriv[0, 0, 2] = self.numeric_deriv(self.eta_s_func, 'h', 0)
        deriv[0, 1, 2] = -self.eta_s.val

        return deriv.tolist()

    def eta_s_char_func(self):
        r"""
        Equation for given isentropic efficiency characteristic of a pump.

        Returns
        -------
        res : ndarray
            Residual value of equation.

            .. math::

                0 = \left( h_{out} - h_{in} \right) \cdot
                \frac{\Delta h_{s,ref}}{\Delta h_{ref}}
                \cdot char\left( \frac{\dot{m}_{in} \cdot
                v_{in}}{\dot{m}_{in,ref} \cdot v_{in,ref}} \right) -
                \left( h_{out,s} - h_{in} \right)
        """
        # actual values
        i = self.inl[0].to_flow()
        o = self.outl[0].to_flow()
        # design values
        i_d = self.inl[0].to_flow_design()

        v_i = v_mix_ph(i, T0=self.inl[0].T.val_SI)

        expr = i[0] * v_i / (i_d[0] * v_mix_ph(i_d))

        return ((o[2] - i[2]) * self.eta_s.design *
                self.eta_s_char.func.evaluate(expr) -
                (self.h_os('post') - i[2]))

    def eta_s_char_deriv(self):
        r"""
        Calculates the matrix of partial derivatives of the isentropic
        efficiency characteristic function.

        Returns
        -------
        deriv : list
            Matrix of partial derivatives.
        """
        deriv = np.zeros((1, 2 + self.num_vars, self.num_fl + 3))

        deriv[0, 0, 0] = self.numeric_deriv(self.eta_s_char_func, 'm', 0)
        deriv[0, 0, 1] = self.numeric_deriv(self.eta_s_char_func, 'p', 0)
        deriv[0, 0, 2] = self.numeric_deriv(self.eta_s_char_func, 'h', 0)
        deriv[0, 1, 1] = self.numeric_deriv(self.eta_s_char_func, 'p', 1)
        deriv[0, 1, 2] = self.numeric_deriv(self.eta_s_char_func, 'h', 1)

        return deriv.tolist()

    def flow_char_func(self):
        r"""
        Equation for given flow characteristic of a pump.

        Returns
        -------
        res : ndarray
            Residual value of equation.

            .. math::

                0 = p_{out} - p_{in} - char\left( \dot{m}_{in}
                \cdot v_{in} \right)
        """
        i = self.inl[0].to_flow()
        o = self.outl[0].to_flow()

        expr = i[0] * v_mix_ph(i, T0=self.inl[0].T.val_SI)

        return o[1] - i[1] - self.flow_char.func.evaluate(expr)

    def flow_char_deriv(self):
        r"""
        Calculates the matrix of partial derivatives of the flow characteristic
        of a pump.

        Returns
        -------
        deriv : list
            Matrix of partial derivatives.
        """
        deriv = np.zeros((1, 2 + self.num_vars, self.num_fl + 3))

        deriv[0, 0, 0] = self.numeric_deriv(self.flow_char_func, 'm', 0)
        deriv[0, 0, 2] = self.numeric_deriv(self.flow_char_func, 'h', 0)
        for i in range(2):
            deriv[0, i, 1] = self.numeric_deriv(self.flow_char_func, 'p', i)

        return deriv.tolist()

    def convergence_check(self, nw):
        r"""
        Performs a convergence check.

        Parameters
        ----------
        nw : tespy.networks.network
            The network object using this component.

        Note
        ----
        Manipulate enthalpies/pressure at inlet and outlet if not specified by
        user to match physically feasible constraints.
        """
        i, o = self.inl, self.outl

        if not o[0].p.val_set and o[0].p.val_SI < i[0].p.val_SI:
            o[0].p.val_SI = o[0].p.val_SI * 2
        if not i[0].p.val_set and o[0].p.val_SI < i[0].p.val_SI:
            i[0].p.val_SI = o[0].p.val_SI * 0.5

        if not o[0].h.val_set and o[0].h.val_SI < i[0].h.val_SI:
            o[0].h.val_SI = o[0].h.val_SI * 1.1
        if not i[0].h.val_set and o[0].h.val_SI < i[0].h.val_SI:
            i[0].h.val_SI = o[0].h.val_SI * 0.9

        if self.flow_char.is_set:
            expr = i[0].m.val_SI * v_mix_ph(i[0].to_flow(), T0=i[0].T.val_SI)

            if expr > self.flow_char.func.x[-1] and not i[0].m.val_set:
                i[0].m.val_SI = (self.flow_char.func.x[-1] /
                                 v_mix_ph(i[0].to_flow(), T0=i[0].T.val_SI))
            elif expr < self.flow_char.func.x[1] and not i[0].m.val_set:
                i[0].m.val_SI = (self.flow_char.func.x[0] /
                                 v_mix_ph(i[0].to_flow(), T0=i[0].T.val_SI))
            else:
                pass

    @staticmethod
    def initialise_source(c, key):
        r"""
        Returns a starting value for pressure and enthalpy at component's
        outlet.

        Parameters
        ----------
        c : tespy.connections.connection
            Connection to perform initialisation on.

        key : str
            Fluid property to retrieve.

        Returns
        -------
        val : float
            Starting value for pressure/enthalpy in SI units.

            .. math::

                val = \begin{cases}
                10^6 & \text{key = 'p'}\\
                3 \cdot 10^5 & \text{key = 'h'}
                \end{cases}
        """
        if key == 'p':
            return 10e5
        elif key == 'h':
            return 3e5

    @staticmethod
    def initialise_target(c, key):
        r"""
        Returns a starting value for pressure and enthalpy at component's
        inlet.

        Parameters
        ----------
        c : tespy.connections.connection
            Connection to perform initialisation on.

        key : str
            Fluid property to retrieve.

        Returns
        -------
        val : float
            Starting value for pressure/enthalpy in SI units.

            .. math::

                val = \begin{cases}
                10^5 & \text{key = 'p'}\\
                2.9 \cdot 10^5 & \text{key = 'h'}
                \end{cases}
        """
        if key == 'p':
            return 1e5
        elif key == 'h':
            return 2.9e5

    def calc_parameters(self):
        r"""
        Postprocessing parameter calculation.
        """
        turbomachine.calc_parameters(self)

        self.eta_s.val = ((self.h_os('post') - self.inl[0].h.val_SI) /
                          (self.outl[0].h.val_SI - self.inl[0].h.val_SI))

        if self.eta_s_char.is_set:
            # get bound errors for isentropic efficiency characteristics
            i = self.inl[0].to_flow()
            i_d = self.inl[0].to_flow_design()
            v_i = v_mix_ph(i, T0=self.inl[0].T.val_SI)
            expr = i[0] * v_i / (i_d[0] * v_mix_ph(i_d))
            self.eta_s_char.func.get_bound_errors(expr, self.label)

        if self.flow_char.is_set:
            # get bound errors for flow characteristics
            i = self.inl[0].to_flow()
            expr = i[0] * v_mix_ph(i, T0=self.inl[0].T.val_SI)
            self.flow_char.func.get_bound_errors(expr, self.label)

        self.check_parameter_bounds()

# %%


class turbine(turbomachine):
    r"""
    Equations

        **mandatory equations**

        - :func:`tespy.components.components.component.fluid_func`
        - :func:`tespy.components.components.component.mass_flow_func`

        **optional equations**

        .. math::

            0 = \dot{m}_{in} \cdot \left( h_{out} - h_{in} \right) - P\\
            0 = pr \cdot p_{in} - p_{out}

        - :func:`tespy.components.turbomachinery.turbine.eta_s_func`

        **additional equations**

        - :func:`tespy.components.turbomachinery.turbine.additional_equations`

    Inlets/Outlets

        - in1
        - out1

    Image

        .. image:: _images/turbine.svg
           :scale: 100 %
           :alt: alternative text
           :align: center

    Parameters
    ----------
    label : str
        The label of the component.

    design : list
        List containing design parameters (stated as String).

    offdesign : list
        List containing offdesign parameters (stated as String).

    P : String/float/tespy.helpers.dc_cp
        Power, :math:`P/\text{W}`

    eta_s : String/float/tespy.helpers.dc_cp
        Isentropic efficiency, :math:`\eta_s/1`

    pr : String/float/tespy.helpers.dc_cp
        Outlet to inlet pressure ratio, :math:`pr/1`

    eta_s_char : str/tespy.helpers.dc_cc
        Characteristic curve for isentropic efficiency, provide x and y values
        or use generic values (e. g. calculated from design case).

    cone : tespy.helpers.dc_cc
        Characteristics for stodolas cone law.

    Example
    -------
    A steam turbine expands 10 kg/s of superheated steam at 550 °C and 110 bar
    to 0,5 bar at the outlet. For example, it is possible to calulate the power
    output and vapour content at the outlet for a given isentropic efficiency.

    >>> from tespy.components import sink, source, turbine
    >>> from tespy.connections import connection
    >>> from tespy.networks import network
    >>> from tespy.tools.data_containers import dc_cc
    >>> import shutil
    >>> fluid_list = ['water']
    >>> nw = network(fluids=fluid_list, p_unit='bar', T_unit='C',
    ...     h_unit='kJ / kg', iterinfo=False)
    >>> si = sink('sink')
    >>> so = source('source')
    >>> t = turbine('turbine')
    >>> t.component()
    'turbine'
    >>> inc = connection(so, 'out1', t, 'in1')
    >>> outg = connection(t, 'out1', si, 'in1')
    >>> nw.add_conns(inc, outg)

    In design conditions the isentropic efficiency is specified. For offdesign
    a characteristic function will be applied, together with Stodola's cone
    law coupling the turbine mass flow to inlet pressure.

    >>> t.set_attr(eta_s=0.9, design=['eta_s'],
    ... offdesign=['eta_s_char', 'cone'])
    >>> inc.set_attr(fluid={'water': 1}, m=10, T=550, p=110, design=['p'])
    >>> outg.set_attr(p=0.5)
    >>> nw.solve('design')
    >>> nw.save('tmp')
    >>> round(t.P.val, 0)
    -10452574.0
    >>> round(outg.x.val, 3)
    0.914
    >>> inc.set_attr(m=8)
    >>> nw.solve('offdesign', design_path='tmp')
    >>> round(t.eta_s.val, 3)
    0.898
    >>> round(inc.p.val, 1)
    88.6
    >>> shutil.rmtree('./tmp', ignore_errors=True)
    """

    @staticmethod
    def component():
        return 'turbine'

    @staticmethod
    def attr():
        return {'P': dc_cp(max_val=0),
                'eta_s': dc_cp(min_val=0, max_val=1),
                'pr': dc_cp(min_val=0, max_val=1),
                'eta_s_char': dc_cc(param='m'),
                'cone': dc_simple(),
                'Sirr': dc_simple()}

    def additional_equations(self):
        r"""
        Calculates vector vec_res with results of additional equations for
        turbine.

        Equations

            **optional equations**

            - :func:`tespy.components.turbomachinery.turbine.eta_s_char_func`
            - :func:`tespy.components.turbomachinery.turbine.cone_func`

        Returns
        -------
        vec_res : list
            Vector of residual values.
        """
        vec_res = []

        ######################################################################
        # derivatives for specified isentropic efficiency characteristics
        if self.eta_s_char.is_set:
            vec_res += [self.eta_s_char_func()]

        ######################################################################
        # equation for specified cone law
        if self.cone.is_set:
            vec_res += [self.cone_func()]

        return vec_res

    def additional_derivatives(self):
        r"""
        Calculates matrix of partial derivatives for given additional
        equations.

        Returns
        -------
        mat_deriv : list
            Matrix of partial derivatives.
        """
        mat_deriv = []

        ######################################################################
        # derivatives for specified isentropic efficiency characteristics
        if self.eta_s_char.is_set:
            mat_deriv += self.eta_s_char_deriv()

        ######################################################################
        # derivatives for specified cone law
        if self.cone.is_set:
            cone_deriv = np.zeros((1, 2 + self.num_vars, self.num_fl + 3))
            cone_deriv[0, 0, 0] = -1
            cone_deriv[0, 0, 1] = self.numeric_deriv(self.cone_func, 'p', 0)
            cone_deriv[0, 0, 2] = self.numeric_deriv(self.cone_func, 'h', 0)
            cone_deriv[0, 1, 2] = self.numeric_deriv(self.cone_func, 'p', 1)
            mat_deriv += cone_deriv.tolist()

        return mat_deriv

    def eta_s_func(self):
        r"""
        Equation for given isentropic efficiency of a turbine.

        Returns
        -------
        res : float
            Residual value of equation.

            .. math::

                0 = -\left( h_{out} - h_{in} \right) +
                \left( h_{out,s} - h_{in} \right) \cdot \eta_{s,e}
        """
        return (-(self.outl[0].h.val_SI - self.inl[0].h.val_SI) +
                (self.h_os('post') - self.inl[0].h.val_SI) *
                self.eta_s.val)

    def eta_s_deriv(self):
        r"""
        Calculates the matrix of partial derivatives of the isentropic
        efficiency function.

        Returns
        -------
        deriv : list
            Matrix of partial derivatives.
        """
        mat_deriv = np.zeros((1, 2 + self.num_vars, self.num_fl + 3))

        mat_deriv[0, 0, 1] = self.numeric_deriv(self.eta_s_func, 'p', 0)
        mat_deriv[0, 1, 1] = self.numeric_deriv(self.eta_s_func, 'p', 1)
        mat_deriv[0, 0, 2] = self.numeric_deriv(self.eta_s_func, 'h', 0)
        mat_deriv[0, 1, 2] = -1

        return mat_deriv.tolist()

    def cone_func(self):
        r"""
        Equation for stodolas cone law.

        Returns
        -------
        res : float
            Residual value of equation.

            .. math::

                0 = \frac{\dot{m}_{in,ref} \cdot p_{in}}{p_{in,ref}} \cdot
                \sqrt{\frac{p_{in,ref} \cdot v_{in}}{p_{in} \cdot v_{in,ref}}}
                \cdot \sqrt{\frac{1 - \left(\frac{p_{out}}{p_{in}} \right)^{2}}
                {1 - \left(\frac{p_{out,ref}}{p_{in,ref}} \right)^{2}}} -
                \dot{m}_{in}
        """
        # actual values
        i = self.inl[0].to_flow()
        o = self.outl[0].to_flow()
        # design values
        i_d = self.inl[0].to_flow_design()
        o_d = self.outl[0].to_flow_design()

        v_i = v_mix_ph(i, T0=self.inl[0].T.val_SI)

        n = 1
        return (- i[0] + i_d[0] * i[1] / i_d[1] *
                np.sqrt(i_d[1] * v_mix_ph(i_d) / (i[1] * v_i)) *
                np.sqrt(abs((1 - (o[1] / i[1]) ** ((n + 1) / n)) /
                        (1 - (o_d[1] / i_d[1]) ** ((n + 1) / n)))))

    def eta_s_char_func(self):
        r"""
        Equation for given isentropic efficiency characteristic of a turbine.

        Returns
        -------
        res : ndarray
            Residual value of equation.

            .. math::

                0 = - \left( h_{out} - h_{in} \right) + \eta_{s,e,0} \cdot
                f\left( expr \right) \cdot \Delta h_{s}
        """
        # actual values
        i = self.inl[0].to_flow()
        o = self.outl[0].to_flow()
        # design values
        i_d = self.inl[0].to_flow_design()
        o_d = self.outl[0].to_flow_design()

        if self.eta_s_char.param == 'dh_s':
            expr = np.sqrt(self.dh_s_ref / (self.h_os('post') - i[2]))
        elif self.eta_s_char.param == 'm':
            expr = i[0] / i_d[0]
        elif self.eta_s_char.param == 'v':
            v_i = v_mix_ph(i, T0=self.inl[0].T.val_SI)
            expr = i[0] * v_i / (i_d[0] * v_mix_ph(i_d))
        elif self.eta_s_char.param == 'pr':
            expr = (o[1] * i_d[1]) / (i[1] * o_d[1])
        else:
            msg = ('Please choose the parameter, you want to link the '
                   'isentropic efficiency to.')
            logging.error(msg)
            raise ValueError(msg)

        return (-(o[2] - i[2]) + self.eta_s.design *
                self.eta_s_char.func.evaluate(expr) *
                (self.h_os('post') - i[2]))

    def eta_s_char_deriv(self):
        r"""
        Calculates the matrix of partial derivatives of the isentropic
        efficiency characteristic function.

        Returns
        -------
        deriv : list
            Matrix of partial derivatives.
        """
        mat_deriv = np.zeros((1, 2 + self.num_vars, self.num_fl + 3))

        mat_deriv[0, 0, 0] = self.numeric_deriv(self.eta_s_char_func, 'm', 0)
        mat_deriv[0, 0, 1] = self.numeric_deriv(self.eta_s_char_func, 'p', 0)
        mat_deriv[0, 0, 2] = self.numeric_deriv(self.eta_s_char_func, 'h', 0)
        mat_deriv[0, 1, 1] = self.numeric_deriv(self.eta_s_char_func, 'p', 1)
        mat_deriv[0, 1, 2] = self.numeric_deriv(self.eta_s_char_func, 'h', 1)

        return mat_deriv.tolist()

    def convergence_check(self, nw):
        r"""
        Performs a convergence check.

        Parameters
        ----------
        nw : tespy.networks.network
            The network object using this component.

        Note
        ----
        Manipulate enthalpies/pressure at inlet and outlet if not specified by
        user to match physically feasible constraints.
        """
        i, o = self.inl, self.outl

        if i[0].init_csv is False:
            if i[0].p.val_SI <= 1e5 and not i[0].p.val_set:
                i[0].p.val_SI = 1e5

            if i[0].h.val_SI < 10e5 and not i[0].h.val_set:
                i[0].h.val_SI = 10e5

        if o[0].init_csv is False:
            if i[0].h.val_SI <= o[0].h.val_SI and not o[0].h.val_set:
                o[0].h.val_SI = i[0].h.val_SI * 0.75

            if i[0].p.val_SI <= o[0].p.val_SI and not o[0].p.val_set:
                o[0].p.val_SI = i[0].p.val_SI / 2

            if o[0].h.val_SI < 5e5 and not o[0].h.val_set:
                o[0].h.val_SI = 5e5

    @staticmethod
    def initialise_source(c, key):
        r"""
        Returns a starting value for pressure and enthalpy at component's
        outlet.

        Parameters
        ----------
        c : tespy.connections.connection
            Connection to perform initialisation on.

        key : str
            Fluid property to retrieve.

        Returns
        -------
        val : float
            Starting value for pressure/enthalpy in SI units.

            .. math::

                val = \begin{cases}
                5 \cdot 10^4 & \text{key = 'p'}\\
                1.5 \cdot 10^6 & \text{key = 'h'}
                \end{cases}
        """
        if key == 'p':
            return 0.5e5
        elif key == 'h':
            return 1.5e6

    @staticmethod
    def initialise_target(c, key):
        r"""
        Returns a starting value for pressure and enthalpy at component's
        inlet.

        Parameters
        ----------
        c : tespy.connections.connection
            Connection to perform initialisation on.

        key : str
            Fluid property to retrieve.

        Returns
        -------
        val : float
            Starting value for pressure/enthalpy in SI units.

            .. math::

                val = \begin{cases}
                2.5 \cdot 10^6 & \text{key = 'p'}\\
                2 \cdot 10^6 & \text{key = 'h'}
                \end{cases}
        """
        if key == 'p':
            return 2.5e6
        elif key == 'h':
            return 2e6

    def calc_parameters(self):
        r"""
        Postprocessing parameter calculation.
        """
        turbomachine.calc_parameters(self)

        self.eta_s.val = ((self.outl[0].h.val_SI - self.inl[0].h.val_SI) /
                          (self.h_os('post') - self.inl[0].h.val_SI))

        if self.eta_s_char.is_set:
            # get bound errors for isentropic efficiency characteristics
            i = self.inl[0].to_flow()
            o = self.outl[0].to_flow()
            i_d = self.inl[0].to_flow_design()
            o_d = self.outl[0].to_flow_design()

            if self.eta_s_char.param == 'dh_s':
                expr = np.sqrt(self.dh_s_ref / (self.h_os('post') - i[2]))
            elif self.eta_s_char.param == 'm':
                expr = i[0] / i_d[0]
            elif self.eta_s_char.param == 'v':
                v_i = v_mix_ph(i, T0=self.inl[0].T.val_SI)
                expr = i[0] * v_i / (i_d[0] * v_mix_ph(i_d))
            elif self.eta_s_char.param == 'pr':
                expr = (o[1] * i_d[1]) / (i[1] * o_d[1])

            self.eta_s_char.func.get_bound_errors(expr, self.label)

        self.check_parameter_bounds()
