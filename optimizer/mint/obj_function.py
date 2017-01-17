from ocelot.optimizer.mint.opt_objects import Target
import numpy as np
import time


class XFELTarget(Target):
    """
    Objective function

    :param mi: Machine interface
    :param dp: Device property
    :param pen_max: 100, maximum penalty
    :param niter: 0, calls number get_penalty()
    :param penalties: [], appending penalty
    :param times: [], appending the time evolution of get_penalty()
    """
    def __init__(self, mi=None, dp=None, eid=None):
        super(XFELTarget, self).__init__(eid=eid)

        self.mi = mi
        self.dp = dp
        self.debug = False
        self.kill = False
        self.pen_max = 100
        self.niter = 0
        self.penalties = []
        self.times = []
        self.alarms = []
        self.values = []

    def get_alarm(self):
        """
        Method to get alarm level (e.g. BLM value).

        alarm level must be normalized: 0 is min, 1 is max

        :return: alarm level
        """
        return 0

    def get_value(self):
        """
        Method to get signal of target function (e.g. SASE signal).

        :return: value
        """
        values = np.array([dev.get_value() for dev in self.devices])
        return 2*np.sum(np.exp(-np.power((values - np.ones_like(values)), 2) / 5.))
        #value = self.mi.get_value(self.eid)

    def get_penalty(self):
        """
        Method to calculate the penalty on the basis of the value and alarm level.

        penalty = -get_value() + alarm()


        :return: penalty
        """
        sase = self.get_value()
        alarm = self.get_alarm()
        if self.debug: print('alarm:', alarm)
        if self.debug: print('sase:', sase)
        pen = 0.0
        if alarm > 1.0:
            return self.pen_max
        if alarm > 0.7:
            return alarm * self.pen_max/2.
        pen += alarm
        pen -= sase
        if self.debug: print('penalty:', pen)
        self.niter += 1
        #print("niter = ", self.niter)
        self.penalties.append(pen)
        self.times.append(time.time())
        self.values.append(sase)
        self.alarms.append(alarm)
        return pen


    def get_spectrum(self):
        return [0, 0]

    def get_stat_params(self):
        #spetrum = self.get_spectrum()
        #ave = np.mean(spetrum[(2599 - 5 * 120):-1])
        #std = np.std(spetrum[(2599 - 5 * 120):-1])
        ave = self.get_value()
        std = 0.1
        return ave, std

    def get_energy(self):
        return 3