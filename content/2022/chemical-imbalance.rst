How to Find Out If You Have A Chemical Imbalance
################################################

:date: 2022-06-30-18:00
:category: tricks-and-tips
:slug: chemical-imbalance
:summary: Finding out why Monte Carlo results are so much higher

.. figure:: images/PumpkinsMellonCollie.jpg
    :align: center
    :target: https://www.hyperviolet.co/blog/behind-the-artwork-smashing-pumpkins-mellon-collie
    :alt: Yep, I'm getting old. I still think about Smashing Pumpkins album covers.

`Massimo Pizol <https://moutreach.science/>`__ just posted an `interesting question <https://stackoverflow.com/questions/72807629/overestimated-monte-carlo-results-in-brightway>`__ on Stack Overflow: Why are the Monte Carlo global warming results for *market for waste paper, sorted* so much higher than the static results? They are around a factor of 100 higher.

I `wrote a notebook showing how I would answer this question here <https://github.com/brightway-lca/brightway2/blob/master/notebooks/Investigating%20interesting%20Monte%20Carlo%20results.ipynb>`__. What are the lessons from this investigation?

First, we need to do a better job thinking about uncertainty. I think that now, thanks to the nice work of Aleksandra Kim (`1 <https://www.sciencedirect.com/science/article/pii/S1364815221003121>`__, `2 <https://pubs.acs.org/doi/full/10.1021/acs.est.1c07438>`__, paper 3 submitted), we have the tools to do systematic global sensitivity analysis. But this relies on quality uncertainty data, otherwise one gets nonsensical results. There are a number of opportunities to improve the modelling of uncertainty, including better parameterization of datasets to reflect correlations between inputs and outputs, the use of measured data instead of fitted PDFs, and using new data sources to quantify uncertainty in market activities. But a very simple and effective good start would be to fix distributions which are extreme and seem to be incorrect (an upper limit of 20 kilograms of inorganic chemicals to produce one kilogram if tissue paper seems wrong?).

Second, we need to do automated data analysis, based on our communities broad base of knowledge and experience. Database providers should be analyzing data using a similar philosophy to test-driven development, where continuous automated testing in a core part of dataset development. As we will need many kinds of tests, we should solicit testing and analysis checks from the broader industrial ecology community. In the example above, a test that compared the average of stochastic results versus the static values for your 400 favorite impact categories would have flagged the datasets for review.

Finally, the interpretation tooling in Brightway needs to get better. In the example above, the recursive analysis function used the static exchange values instead of the Monte Carlo sampled values when deciding which inputs were important, leading to considerable frustration when the extreme triangular distribution sampled values were not apparent as their modes were quite small and fell below the cut-offs. The library *bw2analyzer* has never been given the same love as other Brightway family members, but without interpretation, a core task of life cycle assessment is not possible.
