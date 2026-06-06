Hunting reference flows
#######################

:date: 2026-05-31-20:00
:category: inventory
:slug: what-is-a-reference-flow
:summary: Can we always find a reference flow in a technosphere matrix? Does it matter?
:status: draft

.. figure:: /images/inner-workings.jpg
    :align: center
    :alt: https://www.flickr.com/photos/el_ramon/8109601643/

In this post, we will look at Brightway backwards - from the pure math back to the data entry and storage steps. This post will be long, and go into detail on exactly how Brightway works in April 2025. There is `a companion notebook <https://github.com/cmutel/spatial-assessment-blog/blob/master/notebooks/Backwards.ipynb>`__ which has all the code used here in a single convenient place.


  $$
  \left[\begin{array}{c|cc}
    & \text{Process A} & \text{Process B} \\\hline
  \text{Steel} & -1 & 0 \\
  \text{CO}_2 & 0.5 & 0.3
  \end{array}\right]
  $$
