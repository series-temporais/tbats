from ..abstract import Estimator
from . import Context


class BATS(Estimator):
    """
    BATS estimator used to fit and select best performing model.

    BATS (Exponential smoothing state space model with Box-Cox
    transformation, ARMA errors, Trend and Seasonal components.)

    Model has been described in De Livera, Hyndman & Snyder (2011).

    All of the useful methods have been implemented in parent Estimator class.

    """

    def __init__(self, use_box_cox=None, use_trend=None, use_damped_trend=None,
                 seasonal_periods=None, use_arma_errors=True,
                 show_warnings=True,
                 n_jobs=None, context=None):
        """ Class constructor

        Parameters
        ----------
        use_box_cox: bool or None, optional (default=None)
            If Box-Cox transformation of original series should be applied.
            When None both cases shall be considered and better is selected by AIC.
        use_trend: bool or None, optional (default=None)
            Indicates whether to include a trend or not.
            When None both cases shall be considered and better is selected by AIC.
        use_damped_trend: bool or None, optional (default=None)
            Indicates whether to include a damping parameter in the trend or not.
            Applies only when trend is used.
            When None both cases shall be considered and better is selected by AIC.
        seasonal_periods: iterable or array-like, optional (default=None)
            Length of each of the periods (amount of observations in each period).
            BATS accepts only int values here.
            When None or empty array, non-seasonal model shall be fitted.
        use_arma_errors: bool, optional (default=True)
            When True BATS will try to improve the model by modelling residuals with ARMA.
            Best model will be selected by AIC.
            If False, ARMA residuals modeling will not be considered.
        show_warnings: bool, optional (default=True)
            If warnings should be shown or not.
            Also see Model.warnings variable that contains all model related warnings.
        n_jobs: int, optional (default=None)
            How many jobs to run in parallel when fitting BATS model.
            When not provided BATS shall try to utilize all available cpu cores.
        context: abstract.ContextInterface, optional (default=None)
            For advanced users only. Provide this to override default behaviors
        """
        if context is None:
            context = Context(show_warnings)  # the default BATS context
        super().__init__(context, use_box_cox=use_box_cox, use_trend=use_trend, use_damped_trend=use_damped_trend,
                         seasonal_periods=seasonal_periods, use_arma_errors=use_arma_errors,
                         n_jobs=n_jobs)

    def _normalize_seasonal_periods(self, seasonal_periods):
        """Makes sure periods are of int type"""
        return self._normalize_seasonal_periods_to_type(seasonal_periods, dtype=int)

    def _do_fit(self, y):
        """Checks all allowed parameter combinations in order to choose best model"""
        components_grid = self._prepare_components_grid()
        return self._choose_model_from_possible_component_settings(y, components_grid)
