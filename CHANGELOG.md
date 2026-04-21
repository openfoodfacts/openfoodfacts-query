# Changelog

## [0.4.0](https://github.com/openfoodfacts/openfoodfacts-query/compare/v0.3.1...v0.4.0) (2026-04-21)


### Features

* Add support for all product types ([#289](https://github.com/openfoodfacts/openfoodfacts-query/issues/289)) ([e871a95](https://github.com/openfoodfacts/openfoodfacts-query/commit/e871a952174e28373a59cbde887f786d9a315c6a))


### Bug Fixes

* Potential fix for 1 code quality finding ([#300](https://github.com/openfoodfacts/openfoodfacts-query/issues/300)) ([58ef0ea](https://github.com/openfoodfacts/openfoodfacts-query/commit/58ef0eadfa30805400f23059aa024a5e19897f32))
* Potential fix for 1 code quality finding ([#302](https://github.com/openfoodfacts/openfoodfacts-query/issues/302)) ([40d2b97](https://github.com/openfoodfacts/openfoodfacts-query/commit/40d2b9702cf0924f6d526d954609fc8fb8728452))

## [0.3.1](https://github.com/openfoodfacts/openfoodfacts-query/compare/v0.3.0...v0.3.1) (2026-04-09)


### Bug Fixes

* Cater for invalid rev values ([#293](https://github.com/openfoodfacts/openfoodfacts-query/issues/293)) ([000d47a](https://github.com/openfoodfacts/openfoodfacts-query/commit/000d47aac1fc2b883da85df743492fd9d7fc14a4))
* Cater for scenarios where some products in a batch fail ([#279](https://github.com/openfoodfacts/openfoodfacts-query/issues/279)) ([ebd285d](https://github.com/openfoodfacts/openfoodfacts-query/commit/ebd285d9b1528a3f127d58ad449d578b60d6fb78))
* Move some of the more chatty logging to only happen at the verbose level ([#285](https://github.com/openfoodfacts/openfoodfacts-query/issues/285)) ([b3e27fc](https://github.com/openfoodfacts/openfoodfacts-query/commit/b3e27fc2940b13d595eaaceb23e13429d053524b))

## [0.3.0](https://github.com/openfoodfacts/openfoodfacts-query/compare/v0.2.1...v0.3.0) (2026-03-10)


### Features

* Add more information to the health check ([#276](https://github.com/openfoodfacts/openfoodfacts-query/issues/276)) ([a2a8a42](https://github.com/openfoodfacts/openfoodfacts-query/commit/a2a8a422984e55fd990a4bcb8e02219e49e1bd78))
* replication of database so that it can be queried by superset ([#225](https://github.com/openfoodfacts/openfoodfacts-query/issues/225)) ([c2f1238](https://github.com/openfoodfacts/openfoodfacts-query/commit/c2f12383d6ef6acd263d29cbf2fd28a0dba07cbf))


### Bug Fixes

* Deploy YAML syntax error ([#278](https://github.com/openfoodfacts/openfoodfacts-query/issues/278)) ([a0c202c](https://github.com/openfoodfacts/openfoodfacts-query/commit/a0c202c4a7eb9b8fa85c96dfdb1f1a9b1aa25dd1))
* Don't import nutriments if new nutrition schema is present ([#277](https://github.com/openfoodfacts/openfoodfacts-query/issues/277)) ([6a14645](https://github.com/openfoodfacts/openfoodfacts-query/commit/6a14645d6e0817a1d39af104362891ae1a220f40))
* migration creating superset user ([#274](https://github.com/openfoodfacts/openfoodfacts-query/issues/274)) ([6da1cee](https://github.com/openfoodfacts/openfoodfacts-query/commit/6da1cee6ae061fd2acf1bb2b47d3b171ab066abc))
* Rename container build job as was clashing with pages build ([#270](https://github.com/openfoodfacts/openfoodfacts-query/issues/270)) ([5c2d956](https://github.com/openfoodfacts/openfoodfacts-query/commit/5c2d9560a2bb3ac0ee8ea7d8d46339b7c11958bc))
* Use original action-wait-for-check so does not fail if job not created yet ([#268](https://github.com/openfoodfacts/openfoodfacts-query/issues/268)) ([8ea65d5](https://github.com/openfoodfacts/openfoodfacts-query/commit/8ea65d50b718250ee740ea4512f9e5538f3d563a))

## [0.2.1](https://github.com/openfoodfacts/openfoodfacts-query/compare/v0.2.0...v0.2.1) (2026-03-01)


### Bug Fixes

* Deal with non-numeric nutrient values ([#264](https://github.com/openfoodfacts/openfoodfacts-query/issues/264)) ([bece157](https://github.com/openfoodfacts/openfoodfacts-query/commit/bece157191f2aacfb199a0844d44d35d16573f77))

## [0.2.0](https://github.com/openfoodfacts/openfoodfacts-query/compare/v0.1.10...v0.2.0) (2026-02-18)


### Features

* Populate event tables for developers ([#230](https://github.com/openfoodfacts/openfoodfacts-query/issues/230)) ([f713bfa](https://github.com/openfoodfacts/openfoodfacts-query/commit/f713bfabb527f9b1918bd59bd502633168f57134))
* remove ip from messages ([#247](https://github.com/openfoodfacts/openfoodfacts-query/issues/247)) ([c621888](https://github.com/openfoodfacts/openfoodfacts-query/commit/c62188850bfaf0979909697ce46951932caa9b7d))
* Support new nutrition schema ([#213](https://github.com/openfoodfacts/openfoodfacts-query/issues/213)) ([fd10890](https://github.com/openfoodfacts/openfoodfacts-query/commit/fd1089019b55806602a707257ca8951d8e9a4945))


### Bug Fixes

* Corrected README example ([#187](https://github.com/openfoodfacts/openfoodfacts-query/issues/187)) ([54b127a](https://github.com/openfoodfacts/openfoodfacts-query/commit/54b127afcdf59ca1f7421bc28c88423b6ab045dd))
* Ensure product_countries are reinstated if a deleted product is reinstated ([#251](https://github.com/openfoodfacts/openfoodfacts-query/issues/251)) ([49131df](https://github.com/openfoodfacts/openfoodfacts-query/commit/49131df5657fea7bf4aa9c47367cb01cd390e7b4))


### Documentation

* List events that we subscribe to ([#193](https://github.com/openfoodfacts/openfoodfacts-query/issues/193)) ([74d575c](https://github.com/openfoodfacts/openfoodfacts-query/commit/74d575c0f437ceb97b9abc1a3dcd7999ed659a53))
* Update README.md with note on Good First Issues ([#218](https://github.com/openfoodfacts/openfoodfacts-query/issues/218)) ([6400eb1](https://github.com/openfoodfacts/openfoodfacts-query/commit/6400eb16a0f628d929386b8cd41012f803fa76e1))

## [0.1.8](https://github.com/openfoodfacts/openfoodfacts-query/compare/v0.1.7...v0.1.8) (2025-07-04)


### Bug Fixes

* Reset error count on success ([4861d3f](https://github.com/openfoodfacts/openfoodfacts-query/commit/4861d3fed596eaf178fd127abeba786e4ff9c9a2))
