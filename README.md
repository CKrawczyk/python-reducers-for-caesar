# python-reducers-for-caesar

This is a collection of external reducers written for [caesar](https://github.com/zooniverse/caesar).

## Build/run the app in docker
To run a local version use:
```bash
docker-compose build
docker-compose up
```
and listen on `localhost:5000`.

## run [zappa](https://github.com/Miserlou/Zappa) commands
```bash
docker-compose run aggregation /bin/bash -lc "zappa <cmd>"
```

To deploy to AWS-lambda first update `zappa_settings.json`'s `profile_name` with your `~/.aws/config` profile name and run:
```bash
docker-compose run aggregation /bin/bash -lc "zappa deploy dev"
```
NOTE: the docker container will add your `~/.aws` forlder as a volume.

To update after the first deploy:
```bash
docker-compose run aggregation /bin/bash -lc "zappa update dev"
```

## run tests
To run the tests use:
```bash
docker-compose run aggregation /bin/bash -lc ./bin/test.sh
```

## API
Clustering points:
  - endpoint: `/cluster_points/?eps=5&min_samples=3`
  - This uses [scikitlearn's DBSCAN](http://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html#sklearn.cluster.DBSCAN) to cluster the data points. (NOTE: `eps` is in "pixels")
  - URL args can be set for any of DBSCAN's keywords
  - response contains the original data points, cluster labels, number of clustered points for each label, x and y position (in pixels) of the cluster centers, and values of the covariance matrix for clustered data points for each tool:
    ```js
    {
      T0_tool1_points_x: [1, 2, 3, ...],
      T0_tool1_points_y: [4, 5, 6, ...],
      T0_tool1_cluster_labels: [0, 0, 0, 0, 0, -1, 1, 1, 1, 1, 1, ...],
      T0_tool1_clusters_count: [5, 5, ...],
      T0_tool1_clusters_x: [20, 5, ...],
      T0_tool1_clusters_y: [10, 35, ...],
      T0_tool1_clusters_var_x: [2, 1.5, ...],
      T0_tool1_clusters_var_y: [1.5, 2, ...],
      T0_tool1_clusters_var_x_y: [0.5, -0.5, ...],
      T0_tool2_points...
    }
    ```
