__copyright__ = "Copyright 2022 Fortescue Metals Group Ltd. All rights reserved"

from dataclasses import dataclass
import dataclasses
import pendulum
import uuid

@dataclass
class HaulerCycleDetails:
    id: str = 'haulercycle{}'.format(uuid.uuid1())
    assetId: str = 'DT5402'
    startedAtUtc: str = pendulum.now('UTC').subtract(hours=12, minutes=1).to_iso8601_string()
    endedAtUtc: str = pendulum.now('UTC').subtract(hours=12).to_iso8601_string()
    sourceMaterial: str = None
    sourceLocationXInMeters: float = 0.0
    sourceLocationYInMeters: float = 0.0
    sourceLocationZInMeters: float = 0.0
    destinationLocation: str = 'HAZ01_RP02_0001'
    destinationLocationXInMeters: float = 406492.0
    destinationLocationYInMeters: float = 6467798.0
    destinationLocationZInMeters: float = 17.0
    loaderBucketCumulativePayloadInTonnes: float = 0.0
    loaderBucketLocation: str = None
    loaderBucketLocationXInMeters: float = 0.0
    loaderBucketLocationYInMeters: float = 0.0
    loaderBucketLocationZInMeters: float = 0.0
    loaderBucketMaterial: str = None
    loaderLocation: str = 'HAZ01_01_0500_002_0503_BS05'
    loaderLocationXInMeters: float = 406532.0
    loaderLocationYInMeters: float = 6467853.0
    loaderLocationZInMeters: float = 17.0
    loaderMaterial: str = 'LA'
    loaderPayloadInTonnes: float = 0.0
    defaultPayloadInTonnes: float = 170.0
    sensorPayloadInTonnes: float = 0.0
    sourceLocation: str = None
    dateId: str = pendulum.now().subtract(hours=12).format('YYYYMMDD')
    loadingAssetId: str = 'EX7109'
    operatorId: str = '520848'
    shiftId: str = (pendulum.now().subtract(hours=12).format('YYYYMMDD') if pendulum.now().subtract(hours=12).hour >=6 else pendulum.now().subtract(days=1).format('YYYYMMDD')) + ('D' if pendulum.now().subtract(hours=12).hour >=6 and pendulum.now().hour <18 else 'N')
    loaderBucketMaterialClass: str = None
    loaderMaterialClass: str = 'Ore'
    reportedMaterial: str = 'LA'
    reportedMaterialClass: str = 'Ore'
    reportedTonnes: float = 170.0
    sourceMaterialClass: str = None
    loaderOperatorId: str = None
    specifiedMaterial: str = None
    specifiedPayloadInTonnes: float = 0.0
    specifiedMaterialClass: str = None
    reportedSourceLocation: str = 'HAZ01_01_0500_002_0503_BS05'
    specifiedSourceLocation: str = None
    loaderMaterialOverride: str = None
    loaderMaterialOverrideClass: str = None
    archived: int = 0
    loaderOperatorName: str = ' '
    operatorName: str = 'Adam Burgess'
    materialSourceType: str = 'MiningBlock'
    type: int = 2

    def __init__(self):
        pass

    def __init__(self, assetId:str = 'DT5402', reportedSourceLocation: str = 'HAZ01_01_0500_002_0503_BS05', loadingAssetId: str = 'EX7109', destinationLocation: str='HAZ01_RP02_0001', reportedTonnes:float=170.0, startedAt_hours_offset: int = -12, endedAt_hours_offset: int = -12, startedAt_mins_offset: int = -1, endedAt_mins_offset: int = 0):
        self.id = 'haulercycle{}'.format(uuid.uuid1())
        self.assetId = assetId
        self.startedAtUtc = pendulum.now('UTC').add(hours=startedAt_hours_offset, minutes=endedAt_mins_offset).to_iso8601_string()
        self.endedAtUtc = pendulum.now('UTC').add(hours=endedAt_hours_offset, minutes=endedAt_mins_offset).to_iso8601_string()
        self.sourceMaterial = None
        self.sourceLocationXInMeters = 0.0
        self.sourceLocationYInMeters = 0.0
        self.sourceLocationZInMeters = 0.0
        self.destinationLocation = destinationLocation
        self.destinationLocationXInMeters = 406492.0
        self.destinationLocationYInMeters = 6467798.0
        self.destinationLocationZInMeters = 17.0
        self.loaderBucketCumulativePayloadInTonnes = 0.0
        self.loaderBucketLocation = None
        self.loaderBucketLocationXInMeters = 0.0
        self.loaderBucketLocationYInMeters = 0.0
        self.loaderBucketLocationZInMeters = 0.0
        self.loaderBucketMaterial = None
        self.loaderLocation = 'HAZ01_01_0500_002_0503_BS05'
        self.loaderLocationXInMeters = 406532.0
        self.loaderLocationYInMeters = 6467853.0
        self.loaderLocationZInMeters = 17.0
        self.loaderMaterial = 'LA'
        self.loaderPayloadInTonnes = 0.0
        self.defaultPayloadInTonnes = 170.0
        self.sensorPayloadInTonnes = 0.0
        self.sourceLocation = None
        self.dateId = pendulum.now().add(hours=startedAt_hours_offset, minutes=endedAt_mins_offset).format('YYYYMMDD')
        self.loadingAssetId = loadingAssetId
        self.operatorId = '520848'
        self.shiftId = (pendulum.now().add(hours=startedAt_hours_offset, minutes=endedAt_mins_offset).format('YYYYMMDD') if pendulum.now().add(hours=startedAt_hours_offset, minutes=endedAt_mins_offset).hour >=6 else pendulum.now().add(hours=startedAt_hours_offset, minutes=endedAt_mins_offset).subtract(days=1).format('YYYYMMDD')) + ('D' if pendulum.now().add(hours=startedAt_hours_offset, minutes=endedAt_mins_offset).hour >=6 and pendulum.now().add(hours=startedAt_hours_offset, minutes=endedAt_mins_offset).hour <18 else 'N')
        self.loaderBucketMaterialClass = None
        self.loaderMaterialClass = 'Ore'
        self.reportedMaterial = 'LA'
        self.reportedMaterialClass = 'Ore'
        self.reportedTonnes = reportedTonnes
        self.sourceMaterialClass = None
        self.loaderOperatorId = None
        self.specifiedMaterial = None
        self.specifiedPayloadInTonnes = 0.0
        self.specifiedMaterialClass = None
        self.reportedSourceLocation = reportedSourceLocation
        self.specifiedSourceLocation = None
        self.loaderMaterialOverride = None
        self.loaderMaterialOverrideClass = None
        self.archived = 0
        self.loaderOperatorName = ' '
        self.operatorName = 'Adam Burgess'
        self.materialSourceType = 'MiningBlock'
        self.type = 2