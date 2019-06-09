# colorfulclouds

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![custom_updater][customupdaterbadge]][customupdater]
[![License][license-shield]](LICENSE.md)


_Component to integrate with [colorfulclouds][colorfulclouds]._

此组件对接彩云天气API V2.5，本版本尚在开发中，最终释出的特性与变更未完全确定。如果突然不能用了，请提 issue

**This component will set up the following platforms.**

Platform | Description
-- | --
`weather` |  colorfulclouds 彩云天气 weather 组件.

Demo: lovelace-ui weather-forecast & custom:weather-card

![example][exampleimg]
![example][exampleimg2]

## Installation

*手工安装* 或者使用 *custom_updater*

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `colorfulclouds`.
4. Download _all_ the files from the `custom_components/colorfulclouds/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Add `colorfulclouds` to your HA configuration.

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/colorfulclouds/__init__.py
custom_components/colorfulclouds/weather.py
```

## Example configuration.yaml

```yaml
weather:
  - platform: colorfulclouds
    api_key: YOUR_API_KEY 
    latitude: 30.7046
    longitude: 121.6544
```

## Configuration options

Key | Type | Required | Description
-- | -- | -- | --
`api_key` | `string` | `True` | 彩云天气 API TOKEN
`api_version` | `string` | `False` | 彩云天气 API Version, 默认 V2.5
`latitude` | `string` | `True` | 纬度
`longitude` | `string` | `True` | 经度

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[colorfulclouds]: https://open.caiyunapp.com/%E5%BD%A9%E4%BA%91%E5%A4%A9%E6%B0%94_API/v2.5
[commits-shield]: https://img.shields.io/github/commit-activity/y/jihao/colorfulclouds.svg?style=for-the-badge
[commits]: https://github.com/jihao/colorfulclouds/commits/master
[customupdater]: https://github.com/custom-components/custom_updater
[customupdaterbadge]: https://img.shields.io/badge/custom__updater-true-success.svg?style=for-the-badge

[exampleimg]: example.png
[exampleimg2]: example-entity.png
[license-shield]: https://img.shields.io/github/license/jihao/colorfulclouds.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Joakim%20Sørensen%20%40ludeeus-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/jihao/colorfulclouds.svg?style=for-the-badge
[releases]: https://github.com/jihao/colorfulclouds/releases
