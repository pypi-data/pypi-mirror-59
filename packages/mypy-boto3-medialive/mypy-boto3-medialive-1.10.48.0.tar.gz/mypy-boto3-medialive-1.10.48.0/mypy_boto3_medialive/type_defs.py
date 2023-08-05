"""
Main interface for medialive service type definitions.

Usage::

    from mypy_boto3.medialive.type_defs import HlsId3SegmentTaggingScheduleActionSettingsTypeDef

    data: HlsId3SegmentTaggingScheduleActionSettingsTypeDef = {...}
"""
from __future__ import annotations

import sys
from typing import Any, Dict, List

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "HlsId3SegmentTaggingScheduleActionSettingsTypeDef",
    "HlsTimedMetadataScheduleActionSettingsTypeDef",
    "StartTimecodeTypeDef",
    "StopTimecodeTypeDef",
    "InputClippingSettingsTypeDef",
    "InputSwitchScheduleActionSettingsTypeDef",
    "PipelinePauseStateSettingsTypeDef",
    "PauseStateScheduleActionSettingsTypeDef",
    "Scte35ReturnToNetworkScheduleActionSettingsTypeDef",
    "Scte35SpliceInsertScheduleActionSettingsTypeDef",
    "Scte35DeliveryRestrictionsTypeDef",
    "Scte35SegmentationDescriptorTypeDef",
    "Scte35DescriptorSettingsTypeDef",
    "Scte35DescriptorTypeDef",
    "Scte35TimeSignalScheduleActionSettingsTypeDef",
    "InputLocationTypeDef",
    "StaticImageActivateScheduleActionSettingsTypeDef",
    "StaticImageDeactivateScheduleActionSettingsTypeDef",
    "ScheduleActionSettingsTypeDef",
    "FixedModeScheduleActionStartSettingsTypeDef",
    "FollowModeScheduleActionStartSettingsTypeDef",
    "ScheduleActionStartSettingsTypeDef",
    "ScheduleActionTypeDef",
    "BatchScheduleActionCreateRequestTypeDef",
    "BatchScheduleActionDeleteRequestTypeDef",
    "BatchScheduleActionCreateResultTypeDef",
    "BatchScheduleActionDeleteResultTypeDef",
    "BatchUpdateScheduleResponseTypeDef",
    "ChannelEgressEndpointTypeDef",
    "AacSettingsTypeDef",
    "Ac3SettingsTypeDef",
    "Eac3SettingsTypeDef",
    "Mp2SettingsTypeDef",
    "AudioCodecSettingsTypeDef",
    "AudioNormalizationSettingsTypeDef",
    "InputChannelLevelTypeDef",
    "AudioChannelMappingTypeDef",
    "RemixSettingsTypeDef",
    "AudioDescriptionTypeDef",
    "AvailBlankingTypeDef",
    "Scte35SpliceInsertTypeDef",
    "Scte35TimeSignalAposTypeDef",
    "AvailSettingsTypeDef",
    "AvailConfigurationTypeDef",
    "BlackoutSlateTypeDef",
    "BurnInDestinationSettingsTypeDef",
    "DvbSubDestinationSettingsTypeDef",
    "TtmlDestinationSettingsTypeDef",
    "CaptionDestinationSettingsTypeDef",
    "CaptionDescriptionTypeDef",
    "InputLossBehaviorTypeDef",
    "GlobalConfigurationTypeDef",
    "NielsenConfigurationTypeDef",
    "OutputLocationRefTypeDef",
    "ArchiveGroupSettingsTypeDef",
    "FrameCaptureGroupSettingsTypeDef",
    "CaptionLanguageMappingTypeDef",
    "HlsAkamaiSettingsTypeDef",
    "HlsBasicPutSettingsTypeDef",
    "HlsMediaStoreSettingsTypeDef",
    "HlsWebdavSettingsTypeDef",
    "HlsCdnSettingsTypeDef",
    "StaticKeySettingsTypeDef",
    "KeyProviderSettingsTypeDef",
    "HlsGroupSettingsTypeDef",
    "MediaPackageGroupSettingsTypeDef",
    "MsSmoothGroupSettingsTypeDef",
    "RtmpGroupSettingsTypeDef",
    "UdpGroupSettingsTypeDef",
    "OutputGroupSettingsTypeDef",
    "DvbNitSettingsTypeDef",
    "DvbSdtSettingsTypeDef",
    "DvbTdtSettingsTypeDef",
    "M2tsSettingsTypeDef",
    "ArchiveContainerSettingsTypeDef",
    "ArchiveOutputSettingsTypeDef",
    "FrameCaptureOutputSettingsTypeDef",
    "AudioOnlyHlsSettingsTypeDef",
    "Fmp4HlsSettingsTypeDef",
    "M3u8SettingsTypeDef",
    "StandardHlsSettingsTypeDef",
    "HlsSettingsTypeDef",
    "HlsOutputSettingsTypeDef",
    "MsSmoothOutputSettingsTypeDef",
    "MultiplexOutputSettingsTypeDef",
    "RtmpOutputSettingsTypeDef",
    "FecOutputSettingsTypeDef",
    "UdpContainerSettingsTypeDef",
    "UdpOutputSettingsTypeDef",
    "OutputSettingsTypeDef",
    "OutputTypeDef",
    "OutputGroupTypeDef",
    "TimecodeConfigTypeDef",
    "FrameCaptureSettingsTypeDef",
    "H264ColorSpaceSettingsTypeDef",
    "H264SettingsTypeDef",
    "Hdr10SettingsTypeDef",
    "H265ColorSpaceSettingsTypeDef",
    "H265SettingsTypeDef",
    "VideoCodecSettingsTypeDef",
    "VideoDescriptionTypeDef",
    "EncoderSettingsTypeDef",
    "AudioLanguageSelectionTypeDef",
    "AudioPidSelectionTypeDef",
    "AudioSelectorSettingsTypeDef",
    "AudioSelectorTypeDef",
    "DvbSubSourceSettingsTypeDef",
    "EmbeddedSourceSettingsTypeDef",
    "Scte20SourceSettingsTypeDef",
    "Scte27SourceSettingsTypeDef",
    "TeletextSourceSettingsTypeDef",
    "CaptionSelectorSettingsTypeDef",
    "CaptionSelectorTypeDef",
    "HlsInputSettingsTypeDef",
    "NetworkInputSettingsTypeDef",
    "VideoSelectorPidTypeDef",
    "VideoSelectorProgramIdTypeDef",
    "VideoSelectorSettingsTypeDef",
    "VideoSelectorTypeDef",
    "InputSettingsTypeDef",
    "InputAttachmentTypeDef",
    "InputSpecificationTypeDef",
    "MediaPackageOutputDestinationSettingsTypeDef",
    "MultiplexProgramChannelDestinationSettingsTypeDef",
    "OutputDestinationSettingsTypeDef",
    "OutputDestinationTypeDef",
    "PipelineDetailTypeDef",
    "ChannelTypeDef",
    "CreateChannelResponseTypeDef",
    "InputDestinationVpcTypeDef",
    "InputDestinationTypeDef",
    "InputSourceTypeDef",
    "MediaConnectFlowTypeDef",
    "InputTypeDef",
    "CreateInputResponseTypeDef",
    "InputWhitelistRuleTypeDef",
    "InputSecurityGroupTypeDef",
    "CreateInputSecurityGroupResponseTypeDef",
    "MultiplexProgramPacketIdentifiersMapTypeDef",
    "MultiplexProgramServiceDescriptorTypeDef",
    "MultiplexStatmuxVideoSettingsTypeDef",
    "MultiplexVideoSettingsTypeDef",
    "MultiplexProgramSettingsTypeDef",
    "MultiplexProgramTypeDef",
    "CreateMultiplexProgramResponseTypeDef",
    "MultiplexMediaConnectOutputDestinationSettingsTypeDef",
    "MultiplexOutputDestinationTypeDef",
    "MultiplexSettingsTypeDef",
    "MultiplexTypeDef",
    "CreateMultiplexResponseTypeDef",
    "DeleteChannelResponseTypeDef",
    "DeleteMultiplexProgramResponseTypeDef",
    "DeleteMultiplexResponseTypeDef",
    "ReservationResourceSpecificationTypeDef",
    "DeleteReservationResponseTypeDef",
    "DescribeChannelResponseTypeDef",
    "DescribeInputResponseTypeDef",
    "DescribeInputSecurityGroupResponseTypeDef",
    "DescribeMultiplexProgramResponseTypeDef",
    "DescribeMultiplexResponseTypeDef",
    "DescribeOfferingResponseTypeDef",
    "DescribeReservationResponseTypeDef",
    "DescribeScheduleResponseTypeDef",
    "InputDestinationRequestTypeDef",
    "InputSourceRequestTypeDef",
    "InputVpcRequestTypeDef",
    "InputWhitelistRuleCidrTypeDef",
    "ChannelSummaryTypeDef",
    "ListChannelsResponseTypeDef",
    "ListInputSecurityGroupsResponseTypeDef",
    "ListInputsResponseTypeDef",
    "MultiplexProgramSummaryTypeDef",
    "ListMultiplexProgramsResponseTypeDef",
    "MultiplexSettingsSummaryTypeDef",
    "MultiplexSummaryTypeDef",
    "ListMultiplexesResponseTypeDef",
    "OfferingTypeDef",
    "ListOfferingsResponseTypeDef",
    "ReservationTypeDef",
    "ListReservationsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MediaConnectFlowRequestTypeDef",
    "PaginatorConfigTypeDef",
    "PurchaseOfferingResponseTypeDef",
    "StartChannelResponseTypeDef",
    "StartMultiplexResponseTypeDef",
    "StopChannelResponseTypeDef",
    "StopMultiplexResponseTypeDef",
    "UpdateChannelClassResponseTypeDef",
    "UpdateChannelResponseTypeDef",
    "UpdateInputResponseTypeDef",
    "UpdateInputSecurityGroupResponseTypeDef",
    "UpdateMultiplexProgramResponseTypeDef",
    "UpdateMultiplexResponseTypeDef",
    "UpdateReservationResponseTypeDef",
    "WaiterConfigTypeDef",
)

HlsId3SegmentTaggingScheduleActionSettingsTypeDef = TypedDict(
    "HlsId3SegmentTaggingScheduleActionSettingsTypeDef", {"Tag": str}
)

HlsTimedMetadataScheduleActionSettingsTypeDef = TypedDict(
    "HlsTimedMetadataScheduleActionSettingsTypeDef", {"Id3": str}
)

StartTimecodeTypeDef = TypedDict("StartTimecodeTypeDef", {"Timecode": str}, total=False)

StopTimecodeTypeDef = TypedDict(
    "StopTimecodeTypeDef",
    {
        "LastFrameClippingBehavior": Literal["EXCLUDE_LAST_FRAME", "INCLUDE_LAST_FRAME"],
        "Timecode": str,
    },
    total=False,
)

_RequiredInputClippingSettingsTypeDef = TypedDict(
    "_RequiredInputClippingSettingsTypeDef",
    {"InputTimecodeSource": Literal["ZEROBASED", "EMBEDDED"]},
)
_OptionalInputClippingSettingsTypeDef = TypedDict(
    "_OptionalInputClippingSettingsTypeDef",
    {"StartTimecode": StartTimecodeTypeDef, "StopTimecode": StopTimecodeTypeDef},
    total=False,
)


class InputClippingSettingsTypeDef(
    _RequiredInputClippingSettingsTypeDef, _OptionalInputClippingSettingsTypeDef
):
    pass


_RequiredInputSwitchScheduleActionSettingsTypeDef = TypedDict(
    "_RequiredInputSwitchScheduleActionSettingsTypeDef", {"InputAttachmentNameReference": str}
)
_OptionalInputSwitchScheduleActionSettingsTypeDef = TypedDict(
    "_OptionalInputSwitchScheduleActionSettingsTypeDef",
    {"InputClippingSettings": InputClippingSettingsTypeDef, "UrlPath": List[str]},
    total=False,
)


class InputSwitchScheduleActionSettingsTypeDef(
    _RequiredInputSwitchScheduleActionSettingsTypeDef,
    _OptionalInputSwitchScheduleActionSettingsTypeDef,
):
    pass


PipelinePauseStateSettingsTypeDef = TypedDict(
    "PipelinePauseStateSettingsTypeDef", {"PipelineId": Literal["PIPELINE_0", "PIPELINE_1"]}
)

PauseStateScheduleActionSettingsTypeDef = TypedDict(
    "PauseStateScheduleActionSettingsTypeDef",
    {"Pipelines": List[PipelinePauseStateSettingsTypeDef]},
    total=False,
)

Scte35ReturnToNetworkScheduleActionSettingsTypeDef = TypedDict(
    "Scte35ReturnToNetworkScheduleActionSettingsTypeDef", {"SpliceEventId": int}
)

_RequiredScte35SpliceInsertScheduleActionSettingsTypeDef = TypedDict(
    "_RequiredScte35SpliceInsertScheduleActionSettingsTypeDef", {"SpliceEventId": int}
)
_OptionalScte35SpliceInsertScheduleActionSettingsTypeDef = TypedDict(
    "_OptionalScte35SpliceInsertScheduleActionSettingsTypeDef", {"Duration": int}, total=False
)


class Scte35SpliceInsertScheduleActionSettingsTypeDef(
    _RequiredScte35SpliceInsertScheduleActionSettingsTypeDef,
    _OptionalScte35SpliceInsertScheduleActionSettingsTypeDef,
):
    pass


Scte35DeliveryRestrictionsTypeDef = TypedDict(
    "Scte35DeliveryRestrictionsTypeDef",
    {
        "ArchiveAllowedFlag": Literal["ARCHIVE_NOT_ALLOWED", "ARCHIVE_ALLOWED"],
        "DeviceRestrictions": Literal[
            "NONE", "RESTRICT_GROUP0", "RESTRICT_GROUP1", "RESTRICT_GROUP2"
        ],
        "NoRegionalBlackoutFlag": Literal["REGIONAL_BLACKOUT", "NO_REGIONAL_BLACKOUT"],
        "WebDeliveryAllowedFlag": Literal["WEB_DELIVERY_NOT_ALLOWED", "WEB_DELIVERY_ALLOWED"],
    },
)

_RequiredScte35SegmentationDescriptorTypeDef = TypedDict(
    "_RequiredScte35SegmentationDescriptorTypeDef",
    {
        "SegmentationCancelIndicator": Literal[
            "SEGMENTATION_EVENT_NOT_CANCELED", "SEGMENTATION_EVENT_CANCELED"
        ],
        "SegmentationEventId": int,
    },
)
_OptionalScte35SegmentationDescriptorTypeDef = TypedDict(
    "_OptionalScte35SegmentationDescriptorTypeDef",
    {
        "DeliveryRestrictions": Scte35DeliveryRestrictionsTypeDef,
        "SegmentNum": int,
        "SegmentationDuration": int,
        "SegmentationTypeId": int,
        "SegmentationUpid": str,
        "SegmentationUpidType": int,
        "SegmentsExpected": int,
        "SubSegmentNum": int,
        "SubSegmentsExpected": int,
    },
    total=False,
)


class Scte35SegmentationDescriptorTypeDef(
    _RequiredScte35SegmentationDescriptorTypeDef, _OptionalScte35SegmentationDescriptorTypeDef
):
    pass


Scte35DescriptorSettingsTypeDef = TypedDict(
    "Scte35DescriptorSettingsTypeDef",
    {"SegmentationDescriptorScte35DescriptorSettings": Scte35SegmentationDescriptorTypeDef},
)

Scte35DescriptorTypeDef = TypedDict(
    "Scte35DescriptorTypeDef", {"Scte35DescriptorSettings": Scte35DescriptorSettingsTypeDef}
)

Scte35TimeSignalScheduleActionSettingsTypeDef = TypedDict(
    "Scte35TimeSignalScheduleActionSettingsTypeDef",
    {"Scte35Descriptors": List[Scte35DescriptorTypeDef]},
)

_RequiredInputLocationTypeDef = TypedDict("_RequiredInputLocationTypeDef", {"Uri": str})
_OptionalInputLocationTypeDef = TypedDict(
    "_OptionalInputLocationTypeDef", {"PasswordParam": str, "Username": str}, total=False
)


class InputLocationTypeDef(_RequiredInputLocationTypeDef, _OptionalInputLocationTypeDef):
    pass


_RequiredStaticImageActivateScheduleActionSettingsTypeDef = TypedDict(
    "_RequiredStaticImageActivateScheduleActionSettingsTypeDef", {"Image": InputLocationTypeDef}
)
_OptionalStaticImageActivateScheduleActionSettingsTypeDef = TypedDict(
    "_OptionalStaticImageActivateScheduleActionSettingsTypeDef",
    {
        "Duration": int,
        "FadeIn": int,
        "FadeOut": int,
        "Height": int,
        "ImageX": int,
        "ImageY": int,
        "Layer": int,
        "Opacity": int,
        "Width": int,
    },
    total=False,
)


class StaticImageActivateScheduleActionSettingsTypeDef(
    _RequiredStaticImageActivateScheduleActionSettingsTypeDef,
    _OptionalStaticImageActivateScheduleActionSettingsTypeDef,
):
    pass


StaticImageDeactivateScheduleActionSettingsTypeDef = TypedDict(
    "StaticImageDeactivateScheduleActionSettingsTypeDef",
    {"FadeOut": int, "Layer": int},
    total=False,
)

ScheduleActionSettingsTypeDef = TypedDict(
    "ScheduleActionSettingsTypeDef",
    {
        "HlsId3SegmentTaggingSettings": HlsId3SegmentTaggingScheduleActionSettingsTypeDef,
        "HlsTimedMetadataSettings": HlsTimedMetadataScheduleActionSettingsTypeDef,
        "InputSwitchSettings": InputSwitchScheduleActionSettingsTypeDef,
        "PauseStateSettings": PauseStateScheduleActionSettingsTypeDef,
        "Scte35ReturnToNetworkSettings": Scte35ReturnToNetworkScheduleActionSettingsTypeDef,
        "Scte35SpliceInsertSettings": Scte35SpliceInsertScheduleActionSettingsTypeDef,
        "Scte35TimeSignalSettings": Scte35TimeSignalScheduleActionSettingsTypeDef,
        "StaticImageActivateSettings": StaticImageActivateScheduleActionSettingsTypeDef,
        "StaticImageDeactivateSettings": StaticImageDeactivateScheduleActionSettingsTypeDef,
    },
    total=False,
)

FixedModeScheduleActionStartSettingsTypeDef = TypedDict(
    "FixedModeScheduleActionStartSettingsTypeDef", {"Time": str}
)

FollowModeScheduleActionStartSettingsTypeDef = TypedDict(
    "FollowModeScheduleActionStartSettingsTypeDef",
    {"FollowPoint": Literal["END", "START"], "ReferenceActionName": str},
)

ScheduleActionStartSettingsTypeDef = TypedDict(
    "ScheduleActionStartSettingsTypeDef",
    {
        "FixedModeScheduleActionStartSettings": FixedModeScheduleActionStartSettingsTypeDef,
        "FollowModeScheduleActionStartSettings": FollowModeScheduleActionStartSettingsTypeDef,
        "ImmediateModeScheduleActionStartSettings": Dict[str, Any],
    },
    total=False,
)

ScheduleActionTypeDef = TypedDict(
    "ScheduleActionTypeDef",
    {
        "ActionName": str,
        "ScheduleActionSettings": ScheduleActionSettingsTypeDef,
        "ScheduleActionStartSettings": ScheduleActionStartSettingsTypeDef,
    },
)

BatchScheduleActionCreateRequestTypeDef = TypedDict(
    "BatchScheduleActionCreateRequestTypeDef", {"ScheduleActions": List[ScheduleActionTypeDef]}
)

BatchScheduleActionDeleteRequestTypeDef = TypedDict(
    "BatchScheduleActionDeleteRequestTypeDef", {"ActionNames": List[str]}
)

BatchScheduleActionCreateResultTypeDef = TypedDict(
    "BatchScheduleActionCreateResultTypeDef", {"ScheduleActions": List[ScheduleActionTypeDef]}
)

BatchScheduleActionDeleteResultTypeDef = TypedDict(
    "BatchScheduleActionDeleteResultTypeDef", {"ScheduleActions": List[ScheduleActionTypeDef]}
)

BatchUpdateScheduleResponseTypeDef = TypedDict(
    "BatchUpdateScheduleResponseTypeDef",
    {
        "Creates": BatchScheduleActionCreateResultTypeDef,
        "Deletes": BatchScheduleActionDeleteResultTypeDef,
    },
    total=False,
)

ChannelEgressEndpointTypeDef = TypedDict(
    "ChannelEgressEndpointTypeDef", {"SourceIp": str}, total=False
)

AacSettingsTypeDef = TypedDict(
    "AacSettingsTypeDef",
    {
        "Bitrate": float,
        "CodingMode": Literal[
            "AD_RECEIVER_MIX",
            "CODING_MODE_1_0",
            "CODING_MODE_1_1",
            "CODING_MODE_2_0",
            "CODING_MODE_5_1",
        ],
        "InputType": Literal["BROADCASTER_MIXED_AD", "NORMAL"],
        "Profile": Literal["HEV1", "HEV2", "LC"],
        "RateControlMode": Literal["CBR", "VBR"],
        "RawFormat": Literal["LATM_LOAS", "NONE"],
        "SampleRate": float,
        "Spec": Literal["MPEG2", "MPEG4"],
        "VbrQuality": Literal["HIGH", "LOW", "MEDIUM_HIGH", "MEDIUM_LOW"],
    },
    total=False,
)

Ac3SettingsTypeDef = TypedDict(
    "Ac3SettingsTypeDef",
    {
        "Bitrate": float,
        "BitstreamMode": Literal[
            "COMMENTARY",
            "COMPLETE_MAIN",
            "DIALOGUE",
            "EMERGENCY",
            "HEARING_IMPAIRED",
            "MUSIC_AND_EFFECTS",
            "VISUALLY_IMPAIRED",
            "VOICE_OVER",
        ],
        "CodingMode": Literal[
            "CODING_MODE_1_0", "CODING_MODE_1_1", "CODING_MODE_2_0", "CODING_MODE_3_2_LFE"
        ],
        "Dialnorm": int,
        "DrcProfile": Literal["FILM_STANDARD", "NONE"],
        "LfeFilter": Literal["DISABLED", "ENABLED"],
        "MetadataControl": Literal["FOLLOW_INPUT", "USE_CONFIGURED"],
    },
    total=False,
)

Eac3SettingsTypeDef = TypedDict(
    "Eac3SettingsTypeDef",
    {
        "AttenuationControl": Literal["ATTENUATE_3_DB", "NONE"],
        "Bitrate": float,
        "BitstreamMode": Literal[
            "COMMENTARY", "COMPLETE_MAIN", "EMERGENCY", "HEARING_IMPAIRED", "VISUALLY_IMPAIRED"
        ],
        "CodingMode": Literal["CODING_MODE_1_0", "CODING_MODE_2_0", "CODING_MODE_3_2"],
        "DcFilter": Literal["DISABLED", "ENABLED"],
        "Dialnorm": int,
        "DrcLine": Literal[
            "FILM_LIGHT", "FILM_STANDARD", "MUSIC_LIGHT", "MUSIC_STANDARD", "NONE", "SPEECH"
        ],
        "DrcRf": Literal[
            "FILM_LIGHT", "FILM_STANDARD", "MUSIC_LIGHT", "MUSIC_STANDARD", "NONE", "SPEECH"
        ],
        "LfeControl": Literal["LFE", "NO_LFE"],
        "LfeFilter": Literal["DISABLED", "ENABLED"],
        "LoRoCenterMixLevel": float,
        "LoRoSurroundMixLevel": float,
        "LtRtCenterMixLevel": float,
        "LtRtSurroundMixLevel": float,
        "MetadataControl": Literal["FOLLOW_INPUT", "USE_CONFIGURED"],
        "PassthroughControl": Literal["NO_PASSTHROUGH", "WHEN_POSSIBLE"],
        "PhaseControl": Literal["NO_SHIFT", "SHIFT_90_DEGREES"],
        "StereoDownmix": Literal["DPL2", "LO_RO", "LT_RT", "NOT_INDICATED"],
        "SurroundExMode": Literal["DISABLED", "ENABLED", "NOT_INDICATED"],
        "SurroundMode": Literal["DISABLED", "ENABLED", "NOT_INDICATED"],
    },
    total=False,
)

Mp2SettingsTypeDef = TypedDict(
    "Mp2SettingsTypeDef",
    {
        "Bitrate": float,
        "CodingMode": Literal["CODING_MODE_1_0", "CODING_MODE_2_0"],
        "SampleRate": float,
    },
    total=False,
)

AudioCodecSettingsTypeDef = TypedDict(
    "AudioCodecSettingsTypeDef",
    {
        "AacSettings": AacSettingsTypeDef,
        "Ac3Settings": Ac3SettingsTypeDef,
        "Eac3Settings": Eac3SettingsTypeDef,
        "Mp2Settings": Mp2SettingsTypeDef,
        "PassThroughSettings": Dict[str, Any],
    },
    total=False,
)

AudioNormalizationSettingsTypeDef = TypedDict(
    "AudioNormalizationSettingsTypeDef",
    {
        "Algorithm": Literal["ITU_1770_1", "ITU_1770_2"],
        "AlgorithmControl": Literal["CORRECT_AUDIO"],
        "TargetLkfs": float,
    },
    total=False,
)

InputChannelLevelTypeDef = TypedDict("InputChannelLevelTypeDef", {"Gain": int, "InputChannel": int})

AudioChannelMappingTypeDef = TypedDict(
    "AudioChannelMappingTypeDef",
    {"InputChannelLevels": List[InputChannelLevelTypeDef], "OutputChannel": int},
)

_RequiredRemixSettingsTypeDef = TypedDict(
    "_RequiredRemixSettingsTypeDef", {"ChannelMappings": List[AudioChannelMappingTypeDef]}
)
_OptionalRemixSettingsTypeDef = TypedDict(
    "_OptionalRemixSettingsTypeDef", {"ChannelsIn": int, "ChannelsOut": int}, total=False
)


class RemixSettingsTypeDef(_RequiredRemixSettingsTypeDef, _OptionalRemixSettingsTypeDef):
    pass


_RequiredAudioDescriptionTypeDef = TypedDict(
    "_RequiredAudioDescriptionTypeDef", {"AudioSelectorName": str, "Name": str}
)
_OptionalAudioDescriptionTypeDef = TypedDict(
    "_OptionalAudioDescriptionTypeDef",
    {
        "AudioNormalizationSettings": AudioNormalizationSettingsTypeDef,
        "AudioType": Literal[
            "CLEAN_EFFECTS", "HEARING_IMPAIRED", "UNDEFINED", "VISUAL_IMPAIRED_COMMENTARY"
        ],
        "AudioTypeControl": Literal["FOLLOW_INPUT", "USE_CONFIGURED"],
        "CodecSettings": AudioCodecSettingsTypeDef,
        "LanguageCode": str,
        "LanguageCodeControl": Literal["FOLLOW_INPUT", "USE_CONFIGURED"],
        "RemixSettings": RemixSettingsTypeDef,
        "StreamName": str,
    },
    total=False,
)


class AudioDescriptionTypeDef(_RequiredAudioDescriptionTypeDef, _OptionalAudioDescriptionTypeDef):
    pass


AvailBlankingTypeDef = TypedDict(
    "AvailBlankingTypeDef",
    {"AvailBlankingImage": InputLocationTypeDef, "State": Literal["DISABLED", "ENABLED"]},
    total=False,
)

Scte35SpliceInsertTypeDef = TypedDict(
    "Scte35SpliceInsertTypeDef",
    {
        "AdAvailOffset": int,
        "NoRegionalBlackoutFlag": Literal["FOLLOW", "IGNORE"],
        "WebDeliveryAllowedFlag": Literal["FOLLOW", "IGNORE"],
    },
    total=False,
)

Scte35TimeSignalAposTypeDef = TypedDict(
    "Scte35TimeSignalAposTypeDef",
    {
        "AdAvailOffset": int,
        "NoRegionalBlackoutFlag": Literal["FOLLOW", "IGNORE"],
        "WebDeliveryAllowedFlag": Literal["FOLLOW", "IGNORE"],
    },
    total=False,
)

AvailSettingsTypeDef = TypedDict(
    "AvailSettingsTypeDef",
    {
        "Scte35SpliceInsert": Scte35SpliceInsertTypeDef,
        "Scte35TimeSignalApos": Scte35TimeSignalAposTypeDef,
    },
    total=False,
)

AvailConfigurationTypeDef = TypedDict(
    "AvailConfigurationTypeDef", {"AvailSettings": AvailSettingsTypeDef}, total=False
)

BlackoutSlateTypeDef = TypedDict(
    "BlackoutSlateTypeDef",
    {
        "BlackoutSlateImage": InputLocationTypeDef,
        "NetworkEndBlackout": Literal["DISABLED", "ENABLED"],
        "NetworkEndBlackoutImage": InputLocationTypeDef,
        "NetworkId": str,
        "State": Literal["DISABLED", "ENABLED"],
    },
    total=False,
)

BurnInDestinationSettingsTypeDef = TypedDict(
    "BurnInDestinationSettingsTypeDef",
    {
        "Alignment": Literal["CENTERED", "LEFT", "SMART"],
        "BackgroundColor": Literal["BLACK", "NONE", "WHITE"],
        "BackgroundOpacity": int,
        "Font": InputLocationTypeDef,
        "FontColor": Literal["BLACK", "BLUE", "GREEN", "RED", "WHITE", "YELLOW"],
        "FontOpacity": int,
        "FontResolution": int,
        "FontSize": str,
        "OutlineColor": Literal["BLACK", "BLUE", "GREEN", "RED", "WHITE", "YELLOW"],
        "OutlineSize": int,
        "ShadowColor": Literal["BLACK", "NONE", "WHITE"],
        "ShadowOpacity": int,
        "ShadowXOffset": int,
        "ShadowYOffset": int,
        "TeletextGridControl": Literal["FIXED", "SCALED"],
        "XPosition": int,
        "YPosition": int,
    },
    total=False,
)

DvbSubDestinationSettingsTypeDef = TypedDict(
    "DvbSubDestinationSettingsTypeDef",
    {
        "Alignment": Literal["CENTERED", "LEFT", "SMART"],
        "BackgroundColor": Literal["BLACK", "NONE", "WHITE"],
        "BackgroundOpacity": int,
        "Font": InputLocationTypeDef,
        "FontColor": Literal["BLACK", "BLUE", "GREEN", "RED", "WHITE", "YELLOW"],
        "FontOpacity": int,
        "FontResolution": int,
        "FontSize": str,
        "OutlineColor": Literal["BLACK", "BLUE", "GREEN", "RED", "WHITE", "YELLOW"],
        "OutlineSize": int,
        "ShadowColor": Literal["BLACK", "NONE", "WHITE"],
        "ShadowOpacity": int,
        "ShadowXOffset": int,
        "ShadowYOffset": int,
        "TeletextGridControl": Literal["FIXED", "SCALED"],
        "XPosition": int,
        "YPosition": int,
    },
    total=False,
)

TtmlDestinationSettingsTypeDef = TypedDict(
    "TtmlDestinationSettingsTypeDef",
    {"StyleControl": Literal["PASSTHROUGH", "USE_CONFIGURED"]},
    total=False,
)

CaptionDestinationSettingsTypeDef = TypedDict(
    "CaptionDestinationSettingsTypeDef",
    {
        "AribDestinationSettings": Dict[str, Any],
        "BurnInDestinationSettings": BurnInDestinationSettingsTypeDef,
        "DvbSubDestinationSettings": DvbSubDestinationSettingsTypeDef,
        "EmbeddedDestinationSettings": Dict[str, Any],
        "EmbeddedPlusScte20DestinationSettings": Dict[str, Any],
        "RtmpCaptionInfoDestinationSettings": Dict[str, Any],
        "Scte20PlusEmbeddedDestinationSettings": Dict[str, Any],
        "Scte27DestinationSettings": Dict[str, Any],
        "SmpteTtDestinationSettings": Dict[str, Any],
        "TeletextDestinationSettings": Dict[str, Any],
        "TtmlDestinationSettings": TtmlDestinationSettingsTypeDef,
        "WebvttDestinationSettings": Dict[str, Any],
    },
    total=False,
)

_RequiredCaptionDescriptionTypeDef = TypedDict(
    "_RequiredCaptionDescriptionTypeDef", {"CaptionSelectorName": str, "Name": str}
)
_OptionalCaptionDescriptionTypeDef = TypedDict(
    "_OptionalCaptionDescriptionTypeDef",
    {
        "DestinationSettings": CaptionDestinationSettingsTypeDef,
        "LanguageCode": str,
        "LanguageDescription": str,
    },
    total=False,
)


class CaptionDescriptionTypeDef(
    _RequiredCaptionDescriptionTypeDef, _OptionalCaptionDescriptionTypeDef
):
    pass


InputLossBehaviorTypeDef = TypedDict(
    "InputLossBehaviorTypeDef",
    {
        "BlackFrameMsec": int,
        "InputLossImageColor": str,
        "InputLossImageSlate": InputLocationTypeDef,
        "InputLossImageType": Literal["COLOR", "SLATE"],
        "RepeatFrameMsec": int,
    },
    total=False,
)

GlobalConfigurationTypeDef = TypedDict(
    "GlobalConfigurationTypeDef",
    {
        "InitialAudioGain": int,
        "InputEndAction": Literal["NONE", "SWITCH_AND_LOOP_INPUTS"],
        "InputLossBehavior": InputLossBehaviorTypeDef,
        "OutputLockingMode": Literal["EPOCH_LOCKING", "PIPELINE_LOCKING"],
        "OutputTimingSource": Literal["INPUT_CLOCK", "SYSTEM_CLOCK"],
        "SupportLowFramerateInputs": Literal["DISABLED", "ENABLED"],
    },
    total=False,
)

NielsenConfigurationTypeDef = TypedDict(
    "NielsenConfigurationTypeDef",
    {"DistributorId": str, "NielsenPcmToId3Tagging": Literal["DISABLED", "ENABLED"]},
    total=False,
)

OutputLocationRefTypeDef = TypedDict(
    "OutputLocationRefTypeDef", {"DestinationRefId": str}, total=False
)

_RequiredArchiveGroupSettingsTypeDef = TypedDict(
    "_RequiredArchiveGroupSettingsTypeDef", {"Destination": OutputLocationRefTypeDef}
)
_OptionalArchiveGroupSettingsTypeDef = TypedDict(
    "_OptionalArchiveGroupSettingsTypeDef", {"RolloverInterval": int}, total=False
)


class ArchiveGroupSettingsTypeDef(
    _RequiredArchiveGroupSettingsTypeDef, _OptionalArchiveGroupSettingsTypeDef
):
    pass


FrameCaptureGroupSettingsTypeDef = TypedDict(
    "FrameCaptureGroupSettingsTypeDef", {"Destination": OutputLocationRefTypeDef}
)

CaptionLanguageMappingTypeDef = TypedDict(
    "CaptionLanguageMappingTypeDef",
    {"CaptionChannel": int, "LanguageCode": str, "LanguageDescription": str},
)

HlsAkamaiSettingsTypeDef = TypedDict(
    "HlsAkamaiSettingsTypeDef",
    {
        "ConnectionRetryInterval": int,
        "FilecacheDuration": int,
        "HttpTransferMode": Literal["CHUNKED", "NON_CHUNKED"],
        "NumRetries": int,
        "RestartDelay": int,
        "Salt": str,
        "Token": str,
    },
    total=False,
)

HlsBasicPutSettingsTypeDef = TypedDict(
    "HlsBasicPutSettingsTypeDef",
    {
        "ConnectionRetryInterval": int,
        "FilecacheDuration": int,
        "NumRetries": int,
        "RestartDelay": int,
    },
    total=False,
)

HlsMediaStoreSettingsTypeDef = TypedDict(
    "HlsMediaStoreSettingsTypeDef",
    {
        "ConnectionRetryInterval": int,
        "FilecacheDuration": int,
        "MediaStoreStorageClass": Literal["TEMPORAL"],
        "NumRetries": int,
        "RestartDelay": int,
    },
    total=False,
)

HlsWebdavSettingsTypeDef = TypedDict(
    "HlsWebdavSettingsTypeDef",
    {
        "ConnectionRetryInterval": int,
        "FilecacheDuration": int,
        "HttpTransferMode": Literal["CHUNKED", "NON_CHUNKED"],
        "NumRetries": int,
        "RestartDelay": int,
    },
    total=False,
)

HlsCdnSettingsTypeDef = TypedDict(
    "HlsCdnSettingsTypeDef",
    {
        "HlsAkamaiSettings": HlsAkamaiSettingsTypeDef,
        "HlsBasicPutSettings": HlsBasicPutSettingsTypeDef,
        "HlsMediaStoreSettings": HlsMediaStoreSettingsTypeDef,
        "HlsWebdavSettings": HlsWebdavSettingsTypeDef,
    },
    total=False,
)

_RequiredStaticKeySettingsTypeDef = TypedDict(
    "_RequiredStaticKeySettingsTypeDef", {"StaticKeyValue": str}
)
_OptionalStaticKeySettingsTypeDef = TypedDict(
    "_OptionalStaticKeySettingsTypeDef", {"KeyProviderServer": InputLocationTypeDef}, total=False
)


class StaticKeySettingsTypeDef(
    _RequiredStaticKeySettingsTypeDef, _OptionalStaticKeySettingsTypeDef
):
    pass


KeyProviderSettingsTypeDef = TypedDict(
    "KeyProviderSettingsTypeDef", {"StaticKeySettings": StaticKeySettingsTypeDef}, total=False
)

_RequiredHlsGroupSettingsTypeDef = TypedDict(
    "_RequiredHlsGroupSettingsTypeDef", {"Destination": OutputLocationRefTypeDef}
)
_OptionalHlsGroupSettingsTypeDef = TypedDict(
    "_OptionalHlsGroupSettingsTypeDef",
    {
        "AdMarkers": List[Literal["ADOBE", "ELEMENTAL", "ELEMENTAL_SCTE35"]],
        "BaseUrlContent": str,
        "BaseUrlContent1": str,
        "BaseUrlManifest": str,
        "BaseUrlManifest1": str,
        "CaptionLanguageMappings": List[CaptionLanguageMappingTypeDef],
        "CaptionLanguageSetting": Literal["INSERT", "NONE", "OMIT"],
        "ClientCache": Literal["DISABLED", "ENABLED"],
        "CodecSpecification": Literal["RFC_4281", "RFC_6381"],
        "ConstantIv": str,
        "DirectoryStructure": Literal["SINGLE_DIRECTORY", "SUBDIRECTORY_PER_STREAM"],
        "EncryptionType": Literal["AES128", "SAMPLE_AES"],
        "HlsCdnSettings": HlsCdnSettingsTypeDef,
        "HlsId3SegmentTagging": Literal["DISABLED", "ENABLED"],
        "IFrameOnlyPlaylists": Literal["DISABLED", "STANDARD"],
        "IndexNSegments": int,
        "InputLossAction": Literal["EMIT_OUTPUT", "PAUSE_OUTPUT"],
        "IvInManifest": Literal["EXCLUDE", "INCLUDE"],
        "IvSource": Literal["EXPLICIT", "FOLLOWS_SEGMENT_NUMBER"],
        "KeepSegments": int,
        "KeyFormat": str,
        "KeyFormatVersions": str,
        "KeyProviderSettings": KeyProviderSettingsTypeDef,
        "ManifestCompression": Literal["GZIP", "NONE"],
        "ManifestDurationFormat": Literal["FLOATING_POINT", "INTEGER"],
        "MinSegmentLength": int,
        "Mode": Literal["LIVE", "VOD"],
        "OutputSelection": Literal["MANIFESTS_AND_SEGMENTS", "SEGMENTS_ONLY"],
        "ProgramDateTime": Literal["EXCLUDE", "INCLUDE"],
        "ProgramDateTimePeriod": int,
        "RedundantManifest": Literal["DISABLED", "ENABLED"],
        "SegmentLength": int,
        "SegmentationMode": Literal["USE_INPUT_SEGMENTATION", "USE_SEGMENT_DURATION"],
        "SegmentsPerSubdirectory": int,
        "StreamInfResolution": Literal["EXCLUDE", "INCLUDE"],
        "TimedMetadataId3Frame": Literal["NONE", "PRIV", "TDRL"],
        "TimedMetadataId3Period": int,
        "TimestampDeltaMilliseconds": int,
        "TsFileMode": Literal["SEGMENTED_FILES", "SINGLE_FILE"],
    },
    total=False,
)


class HlsGroupSettingsTypeDef(_RequiredHlsGroupSettingsTypeDef, _OptionalHlsGroupSettingsTypeDef):
    pass


MediaPackageGroupSettingsTypeDef = TypedDict(
    "MediaPackageGroupSettingsTypeDef", {"Destination": OutputLocationRefTypeDef}
)

_RequiredMsSmoothGroupSettingsTypeDef = TypedDict(
    "_RequiredMsSmoothGroupSettingsTypeDef", {"Destination": OutputLocationRefTypeDef}
)
_OptionalMsSmoothGroupSettingsTypeDef = TypedDict(
    "_OptionalMsSmoothGroupSettingsTypeDef",
    {
        "AcquisitionPointId": str,
        "AudioOnlyTimecodeControl": Literal["PASSTHROUGH", "USE_CONFIGURED_CLOCK"],
        "CertificateMode": Literal["SELF_SIGNED", "VERIFY_AUTHENTICITY"],
        "ConnectionRetryInterval": int,
        "EventId": str,
        "EventIdMode": Literal["NO_EVENT_ID", "USE_CONFIGURED", "USE_TIMESTAMP"],
        "EventStopBehavior": Literal["NONE", "SEND_EOS"],
        "FilecacheDuration": int,
        "FragmentLength": int,
        "InputLossAction": Literal["EMIT_OUTPUT", "PAUSE_OUTPUT"],
        "NumRetries": int,
        "RestartDelay": int,
        "SegmentationMode": Literal["USE_INPUT_SEGMENTATION", "USE_SEGMENT_DURATION"],
        "SendDelayMs": int,
        "SparseTrackType": Literal["NONE", "SCTE_35"],
        "StreamManifestBehavior": Literal["DO_NOT_SEND", "SEND"],
        "TimestampOffset": str,
        "TimestampOffsetMode": Literal["USE_CONFIGURED_OFFSET", "USE_EVENT_START_DATE"],
    },
    total=False,
)


class MsSmoothGroupSettingsTypeDef(
    _RequiredMsSmoothGroupSettingsTypeDef, _OptionalMsSmoothGroupSettingsTypeDef
):
    pass


RtmpGroupSettingsTypeDef = TypedDict(
    "RtmpGroupSettingsTypeDef",
    {
        "AuthenticationScheme": Literal["AKAMAI", "COMMON"],
        "CacheFullBehavior": Literal["DISCONNECT_IMMEDIATELY", "WAIT_FOR_SERVER"],
        "CacheLength": int,
        "CaptionData": Literal["ALL", "FIELD1_608", "FIELD1_AND_FIELD2_608"],
        "InputLossAction": Literal["EMIT_OUTPUT", "PAUSE_OUTPUT"],
        "RestartDelay": int,
    },
    total=False,
)

UdpGroupSettingsTypeDef = TypedDict(
    "UdpGroupSettingsTypeDef",
    {
        "InputLossAction": Literal["DROP_PROGRAM", "DROP_TS", "EMIT_PROGRAM"],
        "TimedMetadataId3Frame": Literal["NONE", "PRIV", "TDRL"],
        "TimedMetadataId3Period": int,
    },
    total=False,
)

OutputGroupSettingsTypeDef = TypedDict(
    "OutputGroupSettingsTypeDef",
    {
        "ArchiveGroupSettings": ArchiveGroupSettingsTypeDef,
        "FrameCaptureGroupSettings": FrameCaptureGroupSettingsTypeDef,
        "HlsGroupSettings": HlsGroupSettingsTypeDef,
        "MediaPackageGroupSettings": MediaPackageGroupSettingsTypeDef,
        "MsSmoothGroupSettings": MsSmoothGroupSettingsTypeDef,
        "MultiplexGroupSettings": Dict[str, Any],
        "RtmpGroupSettings": RtmpGroupSettingsTypeDef,
        "UdpGroupSettings": UdpGroupSettingsTypeDef,
    },
    total=False,
)

_RequiredDvbNitSettingsTypeDef = TypedDict(
    "_RequiredDvbNitSettingsTypeDef", {"NetworkId": int, "NetworkName": str}
)
_OptionalDvbNitSettingsTypeDef = TypedDict(
    "_OptionalDvbNitSettingsTypeDef", {"RepInterval": int}, total=False
)


class DvbNitSettingsTypeDef(_RequiredDvbNitSettingsTypeDef, _OptionalDvbNitSettingsTypeDef):
    pass


DvbSdtSettingsTypeDef = TypedDict(
    "DvbSdtSettingsTypeDef",
    {
        "OutputSdt": Literal["SDT_FOLLOW", "SDT_FOLLOW_IF_PRESENT", "SDT_MANUAL", "SDT_NONE"],
        "RepInterval": int,
        "ServiceName": str,
        "ServiceProviderName": str,
    },
    total=False,
)

DvbTdtSettingsTypeDef = TypedDict("DvbTdtSettingsTypeDef", {"RepInterval": int}, total=False)

M2tsSettingsTypeDef = TypedDict(
    "M2tsSettingsTypeDef",
    {
        "AbsentInputAudioBehavior": Literal["DROP", "ENCODE_SILENCE"],
        "Arib": Literal["DISABLED", "ENABLED"],
        "AribCaptionsPid": str,
        "AribCaptionsPidControl": Literal["AUTO", "USE_CONFIGURED"],
        "AudioBufferModel": Literal["ATSC", "DVB"],
        "AudioFramesPerPes": int,
        "AudioPids": str,
        "AudioStreamType": Literal["ATSC", "DVB"],
        "Bitrate": int,
        "BufferModel": Literal["MULTIPLEX", "NONE"],
        "CcDescriptor": Literal["DISABLED", "ENABLED"],
        "DvbNitSettings": DvbNitSettingsTypeDef,
        "DvbSdtSettings": DvbSdtSettingsTypeDef,
        "DvbSubPids": str,
        "DvbTdtSettings": DvbTdtSettingsTypeDef,
        "DvbTeletextPid": str,
        "Ebif": Literal["NONE", "PASSTHROUGH"],
        "EbpAudioInterval": Literal["VIDEO_AND_FIXED_INTERVALS", "VIDEO_INTERVAL"],
        "EbpLookaheadMs": int,
        "EbpPlacement": Literal["VIDEO_AND_AUDIO_PIDS", "VIDEO_PID"],
        "EcmPid": str,
        "EsRateInPes": Literal["EXCLUDE", "INCLUDE"],
        "EtvPlatformPid": str,
        "EtvSignalPid": str,
        "FragmentTime": float,
        "Klv": Literal["NONE", "PASSTHROUGH"],
        "KlvDataPids": str,
        "NielsenId3Behavior": Literal["NO_PASSTHROUGH", "PASSTHROUGH"],
        "NullPacketBitrate": float,
        "PatInterval": int,
        "PcrControl": Literal["CONFIGURED_PCR_PERIOD", "PCR_EVERY_PES_PACKET"],
        "PcrPeriod": int,
        "PcrPid": str,
        "PmtInterval": int,
        "PmtPid": str,
        "ProgramNum": int,
        "RateMode": Literal["CBR", "VBR"],
        "Scte27Pids": str,
        "Scte35Control": Literal["NONE", "PASSTHROUGH"],
        "Scte35Pid": str,
        "SegmentationMarkers": Literal[
            "EBP", "EBP_LEGACY", "NONE", "PSI_SEGSTART", "RAI_ADAPT", "RAI_SEGSTART"
        ],
        "SegmentationStyle": Literal["MAINTAIN_CADENCE", "RESET_CADENCE"],
        "SegmentationTime": float,
        "TimedMetadataBehavior": Literal["NO_PASSTHROUGH", "PASSTHROUGH"],
        "TimedMetadataPid": str,
        "TransportStreamId": int,
        "VideoPid": str,
    },
    total=False,
)

ArchiveContainerSettingsTypeDef = TypedDict(
    "ArchiveContainerSettingsTypeDef", {"M2tsSettings": M2tsSettingsTypeDef}, total=False
)

_RequiredArchiveOutputSettingsTypeDef = TypedDict(
    "_RequiredArchiveOutputSettingsTypeDef", {"ContainerSettings": ArchiveContainerSettingsTypeDef}
)
_OptionalArchiveOutputSettingsTypeDef = TypedDict(
    "_OptionalArchiveOutputSettingsTypeDef", {"Extension": str, "NameModifier": str}, total=False
)


class ArchiveOutputSettingsTypeDef(
    _RequiredArchiveOutputSettingsTypeDef, _OptionalArchiveOutputSettingsTypeDef
):
    pass


FrameCaptureOutputSettingsTypeDef = TypedDict(
    "FrameCaptureOutputSettingsTypeDef", {"NameModifier": str}, total=False
)

AudioOnlyHlsSettingsTypeDef = TypedDict(
    "AudioOnlyHlsSettingsTypeDef",
    {
        "AudioGroupId": str,
        "AudioOnlyImage": InputLocationTypeDef,
        "AudioTrackType": Literal[
            "ALTERNATE_AUDIO_AUTO_SELECT",
            "ALTERNATE_AUDIO_AUTO_SELECT_DEFAULT",
            "ALTERNATE_AUDIO_NOT_AUTO_SELECT",
            "AUDIO_ONLY_VARIANT_STREAM",
        ],
        "SegmentType": Literal["AAC", "FMP4"],
    },
    total=False,
)

Fmp4HlsSettingsTypeDef = TypedDict(
    "Fmp4HlsSettingsTypeDef", {"AudioRenditionSets": str}, total=False
)

M3u8SettingsTypeDef = TypedDict(
    "M3u8SettingsTypeDef",
    {
        "AudioFramesPerPes": int,
        "AudioPids": str,
        "EcmPid": str,
        "NielsenId3Behavior": Literal["NO_PASSTHROUGH", "PASSTHROUGH"],
        "PatInterval": int,
        "PcrControl": Literal["CONFIGURED_PCR_PERIOD", "PCR_EVERY_PES_PACKET"],
        "PcrPeriod": int,
        "PcrPid": str,
        "PmtInterval": int,
        "PmtPid": str,
        "ProgramNum": int,
        "Scte35Behavior": Literal["NO_PASSTHROUGH", "PASSTHROUGH"],
        "Scte35Pid": str,
        "TimedMetadataBehavior": Literal["NO_PASSTHROUGH", "PASSTHROUGH"],
        "TimedMetadataPid": str,
        "TransportStreamId": int,
        "VideoPid": str,
    },
    total=False,
)

_RequiredStandardHlsSettingsTypeDef = TypedDict(
    "_RequiredStandardHlsSettingsTypeDef", {"M3u8Settings": M3u8SettingsTypeDef}
)
_OptionalStandardHlsSettingsTypeDef = TypedDict(
    "_OptionalStandardHlsSettingsTypeDef", {"AudioRenditionSets": str}, total=False
)


class StandardHlsSettingsTypeDef(
    _RequiredStandardHlsSettingsTypeDef, _OptionalStandardHlsSettingsTypeDef
):
    pass


HlsSettingsTypeDef = TypedDict(
    "HlsSettingsTypeDef",
    {
        "AudioOnlyHlsSettings": AudioOnlyHlsSettingsTypeDef,
        "Fmp4HlsSettings": Fmp4HlsSettingsTypeDef,
        "StandardHlsSettings": StandardHlsSettingsTypeDef,
    },
    total=False,
)

_RequiredHlsOutputSettingsTypeDef = TypedDict(
    "_RequiredHlsOutputSettingsTypeDef", {"HlsSettings": HlsSettingsTypeDef}
)
_OptionalHlsOutputSettingsTypeDef = TypedDict(
    "_OptionalHlsOutputSettingsTypeDef",
    {"H265PackagingType": Literal["HEV1", "HVC1"], "NameModifier": str, "SegmentModifier": str},
    total=False,
)


class HlsOutputSettingsTypeDef(
    _RequiredHlsOutputSettingsTypeDef, _OptionalHlsOutputSettingsTypeDef
):
    pass


MsSmoothOutputSettingsTypeDef = TypedDict(
    "MsSmoothOutputSettingsTypeDef",
    {"H265PackagingType": Literal["HEV1", "HVC1"], "NameModifier": str},
    total=False,
)

MultiplexOutputSettingsTypeDef = TypedDict(
    "MultiplexOutputSettingsTypeDef", {"Destination": OutputLocationRefTypeDef}
)

_RequiredRtmpOutputSettingsTypeDef = TypedDict(
    "_RequiredRtmpOutputSettingsTypeDef", {"Destination": OutputLocationRefTypeDef}
)
_OptionalRtmpOutputSettingsTypeDef = TypedDict(
    "_OptionalRtmpOutputSettingsTypeDef",
    {
        "CertificateMode": Literal["SELF_SIGNED", "VERIFY_AUTHENTICITY"],
        "ConnectionRetryInterval": int,
        "NumRetries": int,
    },
    total=False,
)


class RtmpOutputSettingsTypeDef(
    _RequiredRtmpOutputSettingsTypeDef, _OptionalRtmpOutputSettingsTypeDef
):
    pass


FecOutputSettingsTypeDef = TypedDict(
    "FecOutputSettingsTypeDef",
    {"ColumnDepth": int, "IncludeFec": Literal["COLUMN", "COLUMN_AND_ROW"], "RowLength": int},
    total=False,
)

UdpContainerSettingsTypeDef = TypedDict(
    "UdpContainerSettingsTypeDef", {"M2tsSettings": M2tsSettingsTypeDef}, total=False
)

_RequiredUdpOutputSettingsTypeDef = TypedDict(
    "_RequiredUdpOutputSettingsTypeDef",
    {"ContainerSettings": UdpContainerSettingsTypeDef, "Destination": OutputLocationRefTypeDef},
)
_OptionalUdpOutputSettingsTypeDef = TypedDict(
    "_OptionalUdpOutputSettingsTypeDef",
    {"BufferMsec": int, "FecOutputSettings": FecOutputSettingsTypeDef},
    total=False,
)


class UdpOutputSettingsTypeDef(
    _RequiredUdpOutputSettingsTypeDef, _OptionalUdpOutputSettingsTypeDef
):
    pass


OutputSettingsTypeDef = TypedDict(
    "OutputSettingsTypeDef",
    {
        "ArchiveOutputSettings": ArchiveOutputSettingsTypeDef,
        "FrameCaptureOutputSettings": FrameCaptureOutputSettingsTypeDef,
        "HlsOutputSettings": HlsOutputSettingsTypeDef,
        "MediaPackageOutputSettings": Dict[str, Any],
        "MsSmoothOutputSettings": MsSmoothOutputSettingsTypeDef,
        "MultiplexOutputSettings": MultiplexOutputSettingsTypeDef,
        "RtmpOutputSettings": RtmpOutputSettingsTypeDef,
        "UdpOutputSettings": UdpOutputSettingsTypeDef,
    },
    total=False,
)

_RequiredOutputTypeDef = TypedDict(
    "_RequiredOutputTypeDef", {"OutputSettings": OutputSettingsTypeDef}
)
_OptionalOutputTypeDef = TypedDict(
    "_OptionalOutputTypeDef",
    {
        "AudioDescriptionNames": List[str],
        "CaptionDescriptionNames": List[str],
        "OutputName": str,
        "VideoDescriptionName": str,
    },
    total=False,
)


class OutputTypeDef(_RequiredOutputTypeDef, _OptionalOutputTypeDef):
    pass


_RequiredOutputGroupTypeDef = TypedDict(
    "_RequiredOutputGroupTypeDef",
    {"OutputGroupSettings": OutputGroupSettingsTypeDef, "Outputs": List[OutputTypeDef]},
)
_OptionalOutputGroupTypeDef = TypedDict("_OptionalOutputGroupTypeDef", {"Name": str}, total=False)


class OutputGroupTypeDef(_RequiredOutputGroupTypeDef, _OptionalOutputGroupTypeDef):
    pass


_RequiredTimecodeConfigTypeDef = TypedDict(
    "_RequiredTimecodeConfigTypeDef", {"Source": Literal["EMBEDDED", "SYSTEMCLOCK", "ZEROBASED"]}
)
_OptionalTimecodeConfigTypeDef = TypedDict(
    "_OptionalTimecodeConfigTypeDef", {"SyncThreshold": int}, total=False
)


class TimecodeConfigTypeDef(_RequiredTimecodeConfigTypeDef, _OptionalTimecodeConfigTypeDef):
    pass


_RequiredFrameCaptureSettingsTypeDef = TypedDict(
    "_RequiredFrameCaptureSettingsTypeDef", {"CaptureInterval": int}
)
_OptionalFrameCaptureSettingsTypeDef = TypedDict(
    "_OptionalFrameCaptureSettingsTypeDef",
    {"CaptureIntervalUnits": Literal["MILLISECONDS", "SECONDS"]},
    total=False,
)


class FrameCaptureSettingsTypeDef(
    _RequiredFrameCaptureSettingsTypeDef, _OptionalFrameCaptureSettingsTypeDef
):
    pass


H264ColorSpaceSettingsTypeDef = TypedDict(
    "H264ColorSpaceSettingsTypeDef",
    {
        "ColorSpacePassthroughSettings": Dict[str, Any],
        "Rec601Settings": Dict[str, Any],
        "Rec709Settings": Dict[str, Any],
    },
    total=False,
)

H264SettingsTypeDef = TypedDict(
    "H264SettingsTypeDef",
    {
        "AdaptiveQuantization": Literal["HIGH", "HIGHER", "LOW", "MAX", "MEDIUM", "OFF"],
        "AfdSignaling": Literal["AUTO", "FIXED", "NONE"],
        "Bitrate": int,
        "BufFillPct": int,
        "BufSize": int,
        "ColorMetadata": Literal["IGNORE", "INSERT"],
        "ColorSpaceSettings": H264ColorSpaceSettingsTypeDef,
        "EntropyEncoding": Literal["CABAC", "CAVLC"],
        "FixedAfd": Literal[
            "AFD_0000",
            "AFD_0010",
            "AFD_0011",
            "AFD_0100",
            "AFD_1000",
            "AFD_1001",
            "AFD_1010",
            "AFD_1011",
            "AFD_1101",
            "AFD_1110",
            "AFD_1111",
        ],
        "FlickerAq": Literal["DISABLED", "ENABLED"],
        "FramerateControl": Literal["INITIALIZE_FROM_SOURCE", "SPECIFIED"],
        "FramerateDenominator": int,
        "FramerateNumerator": int,
        "GopBReference": Literal["DISABLED", "ENABLED"],
        "GopClosedCadence": int,
        "GopNumBFrames": int,
        "GopSize": float,
        "GopSizeUnits": Literal["FRAMES", "SECONDS"],
        "Level": Literal[
            "H264_LEVEL_1",
            "H264_LEVEL_1_1",
            "H264_LEVEL_1_2",
            "H264_LEVEL_1_3",
            "H264_LEVEL_2",
            "H264_LEVEL_2_1",
            "H264_LEVEL_2_2",
            "H264_LEVEL_3",
            "H264_LEVEL_3_1",
            "H264_LEVEL_3_2",
            "H264_LEVEL_4",
            "H264_LEVEL_4_1",
            "H264_LEVEL_4_2",
            "H264_LEVEL_5",
            "H264_LEVEL_5_1",
            "H264_LEVEL_5_2",
            "H264_LEVEL_AUTO",
        ],
        "LookAheadRateControl": Literal["HIGH", "LOW", "MEDIUM"],
        "MaxBitrate": int,
        "MinIInterval": int,
        "NumRefFrames": int,
        "ParControl": Literal["INITIALIZE_FROM_SOURCE", "SPECIFIED"],
        "ParDenominator": int,
        "ParNumerator": int,
        "Profile": Literal["BASELINE", "HIGH", "HIGH_10BIT", "HIGH_422", "HIGH_422_10BIT", "MAIN"],
        "QvbrQualityLevel": int,
        "RateControlMode": Literal["CBR", "MULTIPLEX", "QVBR", "VBR"],
        "ScanType": Literal["INTERLACED", "PROGRESSIVE"],
        "SceneChangeDetect": Literal["DISABLED", "ENABLED"],
        "Slices": int,
        "Softness": int,
        "SpatialAq": Literal["DISABLED", "ENABLED"],
        "SubgopLength": Literal["DYNAMIC", "FIXED"],
        "Syntax": Literal["DEFAULT", "RP2027"],
        "TemporalAq": Literal["DISABLED", "ENABLED"],
        "TimecodeInsertion": Literal["DISABLED", "PIC_TIMING_SEI"],
    },
    total=False,
)

Hdr10SettingsTypeDef = TypedDict(
    "Hdr10SettingsTypeDef", {"MaxCll": int, "MaxFall": int}, total=False
)

H265ColorSpaceSettingsTypeDef = TypedDict(
    "H265ColorSpaceSettingsTypeDef",
    {
        "ColorSpacePassthroughSettings": Dict[str, Any],
        "Hdr10Settings": Hdr10SettingsTypeDef,
        "Rec601Settings": Dict[str, Any],
        "Rec709Settings": Dict[str, Any],
    },
    total=False,
)

_RequiredH265SettingsTypeDef = TypedDict(
    "_RequiredH265SettingsTypeDef", {"FramerateDenominator": int, "FramerateNumerator": int}
)
_OptionalH265SettingsTypeDef = TypedDict(
    "_OptionalH265SettingsTypeDef",
    {
        "AdaptiveQuantization": Literal["HIGH", "HIGHER", "LOW", "MAX", "MEDIUM", "OFF"],
        "AfdSignaling": Literal["AUTO", "FIXED", "NONE"],
        "AlternativeTransferFunction": Literal["INSERT", "OMIT"],
        "Bitrate": int,
        "BufSize": int,
        "ColorMetadata": Literal["IGNORE", "INSERT"],
        "ColorSpaceSettings": H265ColorSpaceSettingsTypeDef,
        "FixedAfd": Literal[
            "AFD_0000",
            "AFD_0010",
            "AFD_0011",
            "AFD_0100",
            "AFD_1000",
            "AFD_1001",
            "AFD_1010",
            "AFD_1011",
            "AFD_1101",
            "AFD_1110",
            "AFD_1111",
        ],
        "FlickerAq": Literal["DISABLED", "ENABLED"],
        "GopClosedCadence": int,
        "GopSize": float,
        "GopSizeUnits": Literal["FRAMES", "SECONDS"],
        "Level": Literal[
            "H265_LEVEL_1",
            "H265_LEVEL_2",
            "H265_LEVEL_2_1",
            "H265_LEVEL_3",
            "H265_LEVEL_3_1",
            "H265_LEVEL_4",
            "H265_LEVEL_4_1",
            "H265_LEVEL_5",
            "H265_LEVEL_5_1",
            "H265_LEVEL_5_2",
            "H265_LEVEL_6",
            "H265_LEVEL_6_1",
            "H265_LEVEL_6_2",
            "H265_LEVEL_AUTO",
        ],
        "LookAheadRateControl": Literal["HIGH", "LOW", "MEDIUM"],
        "MaxBitrate": int,
        "MinIInterval": int,
        "ParDenominator": int,
        "ParNumerator": int,
        "Profile": Literal["MAIN", "MAIN_10BIT"],
        "QvbrQualityLevel": int,
        "RateControlMode": Literal["CBR", "MULTIPLEX", "QVBR"],
        "ScanType": Literal["PROGRESSIVE"],
        "SceneChangeDetect": Literal["DISABLED", "ENABLED"],
        "Slices": int,
        "Tier": Literal["HIGH", "MAIN"],
        "TimecodeInsertion": Literal["DISABLED", "PIC_TIMING_SEI"],
    },
    total=False,
)


class H265SettingsTypeDef(_RequiredH265SettingsTypeDef, _OptionalH265SettingsTypeDef):
    pass


VideoCodecSettingsTypeDef = TypedDict(
    "VideoCodecSettingsTypeDef",
    {
        "FrameCaptureSettings": FrameCaptureSettingsTypeDef,
        "H264Settings": H264SettingsTypeDef,
        "H265Settings": H265SettingsTypeDef,
    },
    total=False,
)

_RequiredVideoDescriptionTypeDef = TypedDict("_RequiredVideoDescriptionTypeDef", {"Name": str})
_OptionalVideoDescriptionTypeDef = TypedDict(
    "_OptionalVideoDescriptionTypeDef",
    {
        "CodecSettings": VideoCodecSettingsTypeDef,
        "Height": int,
        "RespondToAfd": Literal["NONE", "PASSTHROUGH", "RESPOND"],
        "ScalingBehavior": Literal["DEFAULT", "STRETCH_TO_OUTPUT"],
        "Sharpness": int,
        "Width": int,
    },
    total=False,
)


class VideoDescriptionTypeDef(_RequiredVideoDescriptionTypeDef, _OptionalVideoDescriptionTypeDef):
    pass


_RequiredEncoderSettingsTypeDef = TypedDict(
    "_RequiredEncoderSettingsTypeDef",
    {
        "AudioDescriptions": List[AudioDescriptionTypeDef],
        "OutputGroups": List[OutputGroupTypeDef],
        "TimecodeConfig": TimecodeConfigTypeDef,
        "VideoDescriptions": List[VideoDescriptionTypeDef],
    },
)
_OptionalEncoderSettingsTypeDef = TypedDict(
    "_OptionalEncoderSettingsTypeDef",
    {
        "AvailBlanking": AvailBlankingTypeDef,
        "AvailConfiguration": AvailConfigurationTypeDef,
        "BlackoutSlate": BlackoutSlateTypeDef,
        "CaptionDescriptions": List[CaptionDescriptionTypeDef],
        "GlobalConfiguration": GlobalConfigurationTypeDef,
        "NielsenConfiguration": NielsenConfigurationTypeDef,
    },
    total=False,
)


class EncoderSettingsTypeDef(_RequiredEncoderSettingsTypeDef, _OptionalEncoderSettingsTypeDef):
    pass


_RequiredAudioLanguageSelectionTypeDef = TypedDict(
    "_RequiredAudioLanguageSelectionTypeDef", {"LanguageCode": str}
)
_OptionalAudioLanguageSelectionTypeDef = TypedDict(
    "_OptionalAudioLanguageSelectionTypeDef",
    {"LanguageSelectionPolicy": Literal["LOOSE", "STRICT"]},
    total=False,
)


class AudioLanguageSelectionTypeDef(
    _RequiredAudioLanguageSelectionTypeDef, _OptionalAudioLanguageSelectionTypeDef
):
    pass


AudioPidSelectionTypeDef = TypedDict("AudioPidSelectionTypeDef", {"Pid": int})

AudioSelectorSettingsTypeDef = TypedDict(
    "AudioSelectorSettingsTypeDef",
    {
        "AudioLanguageSelection": AudioLanguageSelectionTypeDef,
        "AudioPidSelection": AudioPidSelectionTypeDef,
    },
    total=False,
)

_RequiredAudioSelectorTypeDef = TypedDict("_RequiredAudioSelectorTypeDef", {"Name": str})
_OptionalAudioSelectorTypeDef = TypedDict(
    "_OptionalAudioSelectorTypeDef", {"SelectorSettings": AudioSelectorSettingsTypeDef}, total=False
)


class AudioSelectorTypeDef(_RequiredAudioSelectorTypeDef, _OptionalAudioSelectorTypeDef):
    pass


DvbSubSourceSettingsTypeDef = TypedDict("DvbSubSourceSettingsTypeDef", {"Pid": int}, total=False)

EmbeddedSourceSettingsTypeDef = TypedDict(
    "EmbeddedSourceSettingsTypeDef",
    {
        "Convert608To708": Literal["DISABLED", "UPCONVERT"],
        "Scte20Detection": Literal["AUTO", "OFF"],
        "Source608ChannelNumber": int,
        "Source608TrackNumber": int,
    },
    total=False,
)

Scte20SourceSettingsTypeDef = TypedDict(
    "Scte20SourceSettingsTypeDef",
    {"Convert608To708": Literal["DISABLED", "UPCONVERT"], "Source608ChannelNumber": int},
    total=False,
)

Scte27SourceSettingsTypeDef = TypedDict("Scte27SourceSettingsTypeDef", {"Pid": int}, total=False)

TeletextSourceSettingsTypeDef = TypedDict(
    "TeletextSourceSettingsTypeDef", {"PageNumber": str}, total=False
)

CaptionSelectorSettingsTypeDef = TypedDict(
    "CaptionSelectorSettingsTypeDef",
    {
        "AribSourceSettings": Dict[str, Any],
        "DvbSubSourceSettings": DvbSubSourceSettingsTypeDef,
        "EmbeddedSourceSettings": EmbeddedSourceSettingsTypeDef,
        "Scte20SourceSettings": Scte20SourceSettingsTypeDef,
        "Scte27SourceSettings": Scte27SourceSettingsTypeDef,
        "TeletextSourceSettings": TeletextSourceSettingsTypeDef,
    },
    total=False,
)

_RequiredCaptionSelectorTypeDef = TypedDict("_RequiredCaptionSelectorTypeDef", {"Name": str})
_OptionalCaptionSelectorTypeDef = TypedDict(
    "_OptionalCaptionSelectorTypeDef",
    {"LanguageCode": str, "SelectorSettings": CaptionSelectorSettingsTypeDef},
    total=False,
)


class CaptionSelectorTypeDef(_RequiredCaptionSelectorTypeDef, _OptionalCaptionSelectorTypeDef):
    pass


HlsInputSettingsTypeDef = TypedDict(
    "HlsInputSettingsTypeDef",
    {"Bandwidth": int, "BufferSegments": int, "Retries": int, "RetryInterval": int},
    total=False,
)

NetworkInputSettingsTypeDef = TypedDict(
    "NetworkInputSettingsTypeDef",
    {
        "HlsInputSettings": HlsInputSettingsTypeDef,
        "ServerValidation": Literal[
            "CHECK_CRYPTOGRAPHY_AND_VALIDATE_NAME", "CHECK_CRYPTOGRAPHY_ONLY"
        ],
    },
    total=False,
)

VideoSelectorPidTypeDef = TypedDict("VideoSelectorPidTypeDef", {"Pid": int}, total=False)

VideoSelectorProgramIdTypeDef = TypedDict(
    "VideoSelectorProgramIdTypeDef", {"ProgramId": int}, total=False
)

VideoSelectorSettingsTypeDef = TypedDict(
    "VideoSelectorSettingsTypeDef",
    {
        "VideoSelectorPid": VideoSelectorPidTypeDef,
        "VideoSelectorProgramId": VideoSelectorProgramIdTypeDef,
    },
    total=False,
)

VideoSelectorTypeDef = TypedDict(
    "VideoSelectorTypeDef",
    {
        "ColorSpace": Literal["FOLLOW", "REC_601", "REC_709"],
        "ColorSpaceUsage": Literal["FALLBACK", "FORCE"],
        "SelectorSettings": VideoSelectorSettingsTypeDef,
    },
    total=False,
)

InputSettingsTypeDef = TypedDict(
    "InputSettingsTypeDef",
    {
        "AudioSelectors": List[AudioSelectorTypeDef],
        "CaptionSelectors": List[CaptionSelectorTypeDef],
        "DeblockFilter": Literal["DISABLED", "ENABLED"],
        "DenoiseFilter": Literal["DISABLED", "ENABLED"],
        "FilterStrength": int,
        "InputFilter": Literal["AUTO", "DISABLED", "FORCED"],
        "NetworkInputSettings": NetworkInputSettingsTypeDef,
        "SourceEndBehavior": Literal["CONTINUE", "LOOP"],
        "VideoSelector": VideoSelectorTypeDef,
    },
    total=False,
)

InputAttachmentTypeDef = TypedDict(
    "InputAttachmentTypeDef",
    {"InputAttachmentName": str, "InputId": str, "InputSettings": InputSettingsTypeDef},
    total=False,
)

InputSpecificationTypeDef = TypedDict(
    "InputSpecificationTypeDef",
    {
        "Codec": Literal["MPEG2", "AVC", "HEVC"],
        "MaximumBitrate": Literal["MAX_10_MBPS", "MAX_20_MBPS", "MAX_50_MBPS"],
        "Resolution": Literal["SD", "HD", "UHD"],
    },
    total=False,
)

MediaPackageOutputDestinationSettingsTypeDef = TypedDict(
    "MediaPackageOutputDestinationSettingsTypeDef", {"ChannelId": str}, total=False
)

MultiplexProgramChannelDestinationSettingsTypeDef = TypedDict(
    "MultiplexProgramChannelDestinationSettingsTypeDef",
    {"MultiplexId": str, "ProgramName": str},
    total=False,
)

OutputDestinationSettingsTypeDef = TypedDict(
    "OutputDestinationSettingsTypeDef",
    {"PasswordParam": str, "StreamName": str, "Url": str, "Username": str},
    total=False,
)

OutputDestinationTypeDef = TypedDict(
    "OutputDestinationTypeDef",
    {
        "Id": str,
        "MediaPackageSettings": List[MediaPackageOutputDestinationSettingsTypeDef],
        "MultiplexSettings": MultiplexProgramChannelDestinationSettingsTypeDef,
        "Settings": List[OutputDestinationSettingsTypeDef],
    },
    total=False,
)

PipelineDetailTypeDef = TypedDict(
    "PipelineDetailTypeDef",
    {"ActiveInputAttachmentName": str, "ActiveInputSwitchActionName": str, "PipelineId": str},
    total=False,
)

ChannelTypeDef = TypedDict(
    "ChannelTypeDef",
    {
        "Arn": str,
        "ChannelClass": Literal["STANDARD", "SINGLE_PIPELINE"],
        "Destinations": List[OutputDestinationTypeDef],
        "EgressEndpoints": List[ChannelEgressEndpointTypeDef],
        "EncoderSettings": EncoderSettingsTypeDef,
        "Id": str,
        "InputAttachments": List[InputAttachmentTypeDef],
        "InputSpecification": InputSpecificationTypeDef,
        "LogLevel": Literal["ERROR", "WARNING", "INFO", "DEBUG", "DISABLED"],
        "Name": str,
        "PipelineDetails": List[PipelineDetailTypeDef],
        "PipelinesRunningCount": int,
        "RoleArn": str,
        "State": Literal[
            "CREATING",
            "CREATE_FAILED",
            "IDLE",
            "STARTING",
            "RUNNING",
            "RECOVERING",
            "STOPPING",
            "DELETING",
            "DELETED",
            "UPDATING",
            "UPDATE_FAILED",
        ],
        "Tags": Dict[str, str],
    },
    total=False,
)

CreateChannelResponseTypeDef = TypedDict(
    "CreateChannelResponseTypeDef", {"Channel": ChannelTypeDef}, total=False
)

InputDestinationVpcTypeDef = TypedDict(
    "InputDestinationVpcTypeDef", {"AvailabilityZone": str, "NetworkInterfaceId": str}, total=False
)

InputDestinationTypeDef = TypedDict(
    "InputDestinationTypeDef",
    {"Ip": str, "Port": str, "Url": str, "Vpc": InputDestinationVpcTypeDef},
    total=False,
)

InputSourceTypeDef = TypedDict(
    "InputSourceTypeDef", {"PasswordParam": str, "Url": str, "Username": str}, total=False
)

MediaConnectFlowTypeDef = TypedDict("MediaConnectFlowTypeDef", {"FlowArn": str}, total=False)

InputTypeDef = TypedDict(
    "InputTypeDef",
    {
        "Arn": str,
        "AttachedChannels": List[str],
        "Destinations": List[InputDestinationTypeDef],
        "Id": str,
        "InputClass": Literal["STANDARD", "SINGLE_PIPELINE"],
        "InputSourceType": Literal["STATIC", "DYNAMIC"],
        "MediaConnectFlows": List[MediaConnectFlowTypeDef],
        "Name": str,
        "RoleArn": str,
        "SecurityGroups": List[str],
        "Sources": List[InputSourceTypeDef],
        "State": Literal["CREATING", "DETACHED", "ATTACHED", "DELETING", "DELETED"],
        "Tags": Dict[str, str],
        "Type": Literal[
            "UDP_PUSH", "RTP_PUSH", "RTMP_PUSH", "RTMP_PULL", "URL_PULL", "MP4_FILE", "MEDIACONNECT"
        ],
    },
    total=False,
)

CreateInputResponseTypeDef = TypedDict(
    "CreateInputResponseTypeDef", {"Input": InputTypeDef}, total=False
)

InputWhitelistRuleTypeDef = TypedDict("InputWhitelistRuleTypeDef", {"Cidr": str}, total=False)

InputSecurityGroupTypeDef = TypedDict(
    "InputSecurityGroupTypeDef",
    {
        "Arn": str,
        "Id": str,
        "Inputs": List[str],
        "State": Literal["IDLE", "IN_USE", "UPDATING", "DELETED"],
        "Tags": Dict[str, str],
        "WhitelistRules": List[InputWhitelistRuleTypeDef],
    },
    total=False,
)

CreateInputSecurityGroupResponseTypeDef = TypedDict(
    "CreateInputSecurityGroupResponseTypeDef",
    {"SecurityGroup": InputSecurityGroupTypeDef},
    total=False,
)

MultiplexProgramPacketIdentifiersMapTypeDef = TypedDict(
    "MultiplexProgramPacketIdentifiersMapTypeDef",
    {
        "AudioPids": List[int],
        "DvbSubPids": List[int],
        "DvbTeletextPid": int,
        "EtvPlatformPid": int,
        "EtvSignalPid": int,
        "KlvDataPids": List[int],
        "PcrPid": int,
        "PmtPid": int,
        "PrivateMetadataPid": int,
        "Scte27Pids": List[int],
        "Scte35Pid": int,
        "TimedMetadataPid": int,
        "VideoPid": int,
    },
    total=False,
)

MultiplexProgramServiceDescriptorTypeDef = TypedDict(
    "MultiplexProgramServiceDescriptorTypeDef", {"ProviderName": str, "ServiceName": str}
)

MultiplexStatmuxVideoSettingsTypeDef = TypedDict(
    "MultiplexStatmuxVideoSettingsTypeDef",
    {"MaximumBitrate": int, "MinimumBitrate": int},
    total=False,
)

MultiplexVideoSettingsTypeDef = TypedDict(
    "MultiplexVideoSettingsTypeDef",
    {"ConstantBitrate": int, "StatmuxSettings": MultiplexStatmuxVideoSettingsTypeDef},
    total=False,
)

_RequiredMultiplexProgramSettingsTypeDef = TypedDict(
    "_RequiredMultiplexProgramSettingsTypeDef", {"ProgramNumber": int}
)
_OptionalMultiplexProgramSettingsTypeDef = TypedDict(
    "_OptionalMultiplexProgramSettingsTypeDef",
    {
        "ServiceDescriptor": MultiplexProgramServiceDescriptorTypeDef,
        "VideoSettings": MultiplexVideoSettingsTypeDef,
    },
    total=False,
)


class MultiplexProgramSettingsTypeDef(
    _RequiredMultiplexProgramSettingsTypeDef, _OptionalMultiplexProgramSettingsTypeDef
):
    pass


MultiplexProgramTypeDef = TypedDict(
    "MultiplexProgramTypeDef",
    {
        "ChannelId": str,
        "MultiplexProgramSettings": MultiplexProgramSettingsTypeDef,
        "PacketIdentifiersMap": MultiplexProgramPacketIdentifiersMapTypeDef,
        "ProgramName": str,
    },
    total=False,
)

CreateMultiplexProgramResponseTypeDef = TypedDict(
    "CreateMultiplexProgramResponseTypeDef",
    {"MultiplexProgram": MultiplexProgramTypeDef},
    total=False,
)

MultiplexMediaConnectOutputDestinationSettingsTypeDef = TypedDict(
    "MultiplexMediaConnectOutputDestinationSettingsTypeDef", {"EntitlementArn": str}, total=False
)

MultiplexOutputDestinationTypeDef = TypedDict(
    "MultiplexOutputDestinationTypeDef",
    {"MediaConnectSettings": MultiplexMediaConnectOutputDestinationSettingsTypeDef},
    total=False,
)

_RequiredMultiplexSettingsTypeDef = TypedDict(
    "_RequiredMultiplexSettingsTypeDef", {"TransportStreamBitrate": int, "TransportStreamId": int}
)
_OptionalMultiplexSettingsTypeDef = TypedDict(
    "_OptionalMultiplexSettingsTypeDef",
    {"MaximumVideoBufferDelayMilliseconds": int, "TransportStreamReservedBitrate": int},
    total=False,
)


class MultiplexSettingsTypeDef(
    _RequiredMultiplexSettingsTypeDef, _OptionalMultiplexSettingsTypeDef
):
    pass


MultiplexTypeDef = TypedDict(
    "MultiplexTypeDef",
    {
        "Arn": str,
        "AvailabilityZones": List[str],
        "Destinations": List[MultiplexOutputDestinationTypeDef],
        "Id": str,
        "MultiplexSettings": MultiplexSettingsTypeDef,
        "Name": str,
        "PipelinesRunningCount": int,
        "ProgramCount": int,
        "State": Literal[
            "CREATING",
            "CREATE_FAILED",
            "IDLE",
            "STARTING",
            "RUNNING",
            "RECOVERING",
            "STOPPING",
            "DELETING",
            "DELETED",
        ],
        "Tags": Dict[str, str],
    },
    total=False,
)

CreateMultiplexResponseTypeDef = TypedDict(
    "CreateMultiplexResponseTypeDef", {"Multiplex": MultiplexTypeDef}, total=False
)

DeleteChannelResponseTypeDef = TypedDict(
    "DeleteChannelResponseTypeDef",
    {
        "Arn": str,
        "ChannelClass": Literal["STANDARD", "SINGLE_PIPELINE"],
        "Destinations": List[OutputDestinationTypeDef],
        "EgressEndpoints": List[ChannelEgressEndpointTypeDef],
        "EncoderSettings": EncoderSettingsTypeDef,
        "Id": str,
        "InputAttachments": List[InputAttachmentTypeDef],
        "InputSpecification": InputSpecificationTypeDef,
        "LogLevel": Literal["ERROR", "WARNING", "INFO", "DEBUG", "DISABLED"],
        "Name": str,
        "PipelineDetails": List[PipelineDetailTypeDef],
        "PipelinesRunningCount": int,
        "RoleArn": str,
        "State": Literal[
            "CREATING",
            "CREATE_FAILED",
            "IDLE",
            "STARTING",
            "RUNNING",
            "RECOVERING",
            "STOPPING",
            "DELETING",
            "DELETED",
            "UPDATING",
            "UPDATE_FAILED",
        ],
        "Tags": Dict[str, str],
    },
    total=False,
)

DeleteMultiplexProgramResponseTypeDef = TypedDict(
    "DeleteMultiplexProgramResponseTypeDef",
    {
        "ChannelId": str,
        "MultiplexProgramSettings": MultiplexProgramSettingsTypeDef,
        "PacketIdentifiersMap": MultiplexProgramPacketIdentifiersMapTypeDef,
        "ProgramName": str,
    },
    total=False,
)

DeleteMultiplexResponseTypeDef = TypedDict(
    "DeleteMultiplexResponseTypeDef",
    {
        "Arn": str,
        "AvailabilityZones": List[str],
        "Destinations": List[MultiplexOutputDestinationTypeDef],
        "Id": str,
        "MultiplexSettings": MultiplexSettingsTypeDef,
        "Name": str,
        "PipelinesRunningCount": int,
        "ProgramCount": int,
        "State": Literal[
            "CREATING",
            "CREATE_FAILED",
            "IDLE",
            "STARTING",
            "RUNNING",
            "RECOVERING",
            "STOPPING",
            "DELETING",
            "DELETED",
        ],
        "Tags": Dict[str, str],
    },
    total=False,
)

ReservationResourceSpecificationTypeDef = TypedDict(
    "ReservationResourceSpecificationTypeDef",
    {
        "ChannelClass": Literal["STANDARD", "SINGLE_PIPELINE"],
        "Codec": Literal["MPEG2", "AVC", "HEVC", "AUDIO"],
        "MaximumBitrate": Literal["MAX_10_MBPS", "MAX_20_MBPS", "MAX_50_MBPS"],
        "MaximumFramerate": Literal["MAX_30_FPS", "MAX_60_FPS"],
        "Resolution": Literal["SD", "HD", "FHD", "UHD"],
        "ResourceType": Literal["INPUT", "OUTPUT", "MULTIPLEX", "CHANNEL"],
        "SpecialFeature": Literal["ADVANCED_AUDIO", "AUDIO_NORMALIZATION"],
        "VideoQuality": Literal["STANDARD", "ENHANCED", "PREMIUM"],
    },
    total=False,
)

DeleteReservationResponseTypeDef = TypedDict(
    "DeleteReservationResponseTypeDef",
    {
        "Arn": str,
        "Count": int,
        "CurrencyCode": str,
        "Duration": int,
        "DurationUnits": Literal["MONTHS"],
        "End": str,
        "FixedPrice": float,
        "Name": str,
        "OfferingDescription": str,
        "OfferingId": str,
        "OfferingType": Literal["NO_UPFRONT"],
        "Region": str,
        "ReservationId": str,
        "ResourceSpecification": ReservationResourceSpecificationTypeDef,
        "Start": str,
        "State": Literal["ACTIVE", "EXPIRED", "CANCELED", "DELETED"],
        "Tags": Dict[str, str],
        "UsagePrice": float,
    },
    total=False,
)

DescribeChannelResponseTypeDef = TypedDict(
    "DescribeChannelResponseTypeDef",
    {
        "Arn": str,
        "ChannelClass": Literal["STANDARD", "SINGLE_PIPELINE"],
        "Destinations": List[OutputDestinationTypeDef],
        "EgressEndpoints": List[ChannelEgressEndpointTypeDef],
        "EncoderSettings": EncoderSettingsTypeDef,
        "Id": str,
        "InputAttachments": List[InputAttachmentTypeDef],
        "InputSpecification": InputSpecificationTypeDef,
        "LogLevel": Literal["ERROR", "WARNING", "INFO", "DEBUG", "DISABLED"],
        "Name": str,
        "PipelineDetails": List[PipelineDetailTypeDef],
        "PipelinesRunningCount": int,
        "RoleArn": str,
        "State": Literal[
            "CREATING",
            "CREATE_FAILED",
            "IDLE",
            "STARTING",
            "RUNNING",
            "RECOVERING",
            "STOPPING",
            "DELETING",
            "DELETED",
            "UPDATING",
            "UPDATE_FAILED",
        ],
        "Tags": Dict[str, str],
    },
    total=False,
)

DescribeInputResponseTypeDef = TypedDict(
    "DescribeInputResponseTypeDef",
    {
        "Arn": str,
        "AttachedChannels": List[str],
        "Destinations": List[InputDestinationTypeDef],
        "Id": str,
        "InputClass": Literal["STANDARD", "SINGLE_PIPELINE"],
        "InputSourceType": Literal["STATIC", "DYNAMIC"],
        "MediaConnectFlows": List[MediaConnectFlowTypeDef],
        "Name": str,
        "RoleArn": str,
        "SecurityGroups": List[str],
        "Sources": List[InputSourceTypeDef],
        "State": Literal["CREATING", "DETACHED", "ATTACHED", "DELETING", "DELETED"],
        "Tags": Dict[str, str],
        "Type": Literal[
            "UDP_PUSH", "RTP_PUSH", "RTMP_PUSH", "RTMP_PULL", "URL_PULL", "MP4_FILE", "MEDIACONNECT"
        ],
    },
    total=False,
)

DescribeInputSecurityGroupResponseTypeDef = TypedDict(
    "DescribeInputSecurityGroupResponseTypeDef",
    {
        "Arn": str,
        "Id": str,
        "Inputs": List[str],
        "State": Literal["IDLE", "IN_USE", "UPDATING", "DELETED"],
        "Tags": Dict[str, str],
        "WhitelistRules": List[InputWhitelistRuleTypeDef],
    },
    total=False,
)

DescribeMultiplexProgramResponseTypeDef = TypedDict(
    "DescribeMultiplexProgramResponseTypeDef",
    {
        "ChannelId": str,
        "MultiplexProgramSettings": MultiplexProgramSettingsTypeDef,
        "PacketIdentifiersMap": MultiplexProgramPacketIdentifiersMapTypeDef,
        "ProgramName": str,
    },
    total=False,
)

DescribeMultiplexResponseTypeDef = TypedDict(
    "DescribeMultiplexResponseTypeDef",
    {
        "Arn": str,
        "AvailabilityZones": List[str],
        "Destinations": List[MultiplexOutputDestinationTypeDef],
        "Id": str,
        "MultiplexSettings": MultiplexSettingsTypeDef,
        "Name": str,
        "PipelinesRunningCount": int,
        "ProgramCount": int,
        "State": Literal[
            "CREATING",
            "CREATE_FAILED",
            "IDLE",
            "STARTING",
            "RUNNING",
            "RECOVERING",
            "STOPPING",
            "DELETING",
            "DELETED",
        ],
        "Tags": Dict[str, str],
    },
    total=False,
)

DescribeOfferingResponseTypeDef = TypedDict(
    "DescribeOfferingResponseTypeDef",
    {
        "Arn": str,
        "CurrencyCode": str,
        "Duration": int,
        "DurationUnits": Literal["MONTHS"],
        "FixedPrice": float,
        "OfferingDescription": str,
        "OfferingId": str,
        "OfferingType": Literal["NO_UPFRONT"],
        "Region": str,
        "ResourceSpecification": ReservationResourceSpecificationTypeDef,
        "UsagePrice": float,
    },
    total=False,
)

DescribeReservationResponseTypeDef = TypedDict(
    "DescribeReservationResponseTypeDef",
    {
        "Arn": str,
        "Count": int,
        "CurrencyCode": str,
        "Duration": int,
        "DurationUnits": Literal["MONTHS"],
        "End": str,
        "FixedPrice": float,
        "Name": str,
        "OfferingDescription": str,
        "OfferingId": str,
        "OfferingType": Literal["NO_UPFRONT"],
        "Region": str,
        "ReservationId": str,
        "ResourceSpecification": ReservationResourceSpecificationTypeDef,
        "Start": str,
        "State": Literal["ACTIVE", "EXPIRED", "CANCELED", "DELETED"],
        "Tags": Dict[str, str],
        "UsagePrice": float,
    },
    total=False,
)

DescribeScheduleResponseTypeDef = TypedDict(
    "DescribeScheduleResponseTypeDef",
    {"NextToken": str, "ScheduleActions": List[ScheduleActionTypeDef]},
    total=False,
)

InputDestinationRequestTypeDef = TypedDict(
    "InputDestinationRequestTypeDef", {"StreamName": str}, total=False
)

InputSourceRequestTypeDef = TypedDict(
    "InputSourceRequestTypeDef", {"PasswordParam": str, "Url": str, "Username": str}, total=False
)

_RequiredInputVpcRequestTypeDef = TypedDict(
    "_RequiredInputVpcRequestTypeDef", {"SubnetIds": List[str]}
)
_OptionalInputVpcRequestTypeDef = TypedDict(
    "_OptionalInputVpcRequestTypeDef", {"SecurityGroupIds": List[str]}, total=False
)


class InputVpcRequestTypeDef(_RequiredInputVpcRequestTypeDef, _OptionalInputVpcRequestTypeDef):
    pass


InputWhitelistRuleCidrTypeDef = TypedDict(
    "InputWhitelistRuleCidrTypeDef", {"Cidr": str}, total=False
)

ChannelSummaryTypeDef = TypedDict(
    "ChannelSummaryTypeDef",
    {
        "Arn": str,
        "ChannelClass": Literal["STANDARD", "SINGLE_PIPELINE"],
        "Destinations": List[OutputDestinationTypeDef],
        "EgressEndpoints": List[ChannelEgressEndpointTypeDef],
        "Id": str,
        "InputAttachments": List[InputAttachmentTypeDef],
        "InputSpecification": InputSpecificationTypeDef,
        "LogLevel": Literal["ERROR", "WARNING", "INFO", "DEBUG", "DISABLED"],
        "Name": str,
        "PipelinesRunningCount": int,
        "RoleArn": str,
        "State": Literal[
            "CREATING",
            "CREATE_FAILED",
            "IDLE",
            "STARTING",
            "RUNNING",
            "RECOVERING",
            "STOPPING",
            "DELETING",
            "DELETED",
            "UPDATING",
            "UPDATE_FAILED",
        ],
        "Tags": Dict[str, str],
    },
    total=False,
)

ListChannelsResponseTypeDef = TypedDict(
    "ListChannelsResponseTypeDef",
    {"Channels": List[ChannelSummaryTypeDef], "NextToken": str},
    total=False,
)

ListInputSecurityGroupsResponseTypeDef = TypedDict(
    "ListInputSecurityGroupsResponseTypeDef",
    {"InputSecurityGroups": List[InputSecurityGroupTypeDef], "NextToken": str},
    total=False,
)

ListInputsResponseTypeDef = TypedDict(
    "ListInputsResponseTypeDef", {"Inputs": List[InputTypeDef], "NextToken": str}, total=False
)

MultiplexProgramSummaryTypeDef = TypedDict(
    "MultiplexProgramSummaryTypeDef", {"ChannelId": str, "ProgramName": str}, total=False
)

ListMultiplexProgramsResponseTypeDef = TypedDict(
    "ListMultiplexProgramsResponseTypeDef",
    {"MultiplexPrograms": List[MultiplexProgramSummaryTypeDef], "NextToken": str},
    total=False,
)

MultiplexSettingsSummaryTypeDef = TypedDict(
    "MultiplexSettingsSummaryTypeDef", {"TransportStreamBitrate": int}, total=False
)

MultiplexSummaryTypeDef = TypedDict(
    "MultiplexSummaryTypeDef",
    {
        "Arn": str,
        "AvailabilityZones": List[str],
        "Id": str,
        "MultiplexSettings": MultiplexSettingsSummaryTypeDef,
        "Name": str,
        "PipelinesRunningCount": int,
        "ProgramCount": int,
        "State": Literal[
            "CREATING",
            "CREATE_FAILED",
            "IDLE",
            "STARTING",
            "RUNNING",
            "RECOVERING",
            "STOPPING",
            "DELETING",
            "DELETED",
        ],
        "Tags": Dict[str, str],
    },
    total=False,
)

ListMultiplexesResponseTypeDef = TypedDict(
    "ListMultiplexesResponseTypeDef",
    {"Multiplexes": List[MultiplexSummaryTypeDef], "NextToken": str},
    total=False,
)

OfferingTypeDef = TypedDict(
    "OfferingTypeDef",
    {
        "Arn": str,
        "CurrencyCode": str,
        "Duration": int,
        "DurationUnits": Literal["MONTHS"],
        "FixedPrice": float,
        "OfferingDescription": str,
        "OfferingId": str,
        "OfferingType": Literal["NO_UPFRONT"],
        "Region": str,
        "ResourceSpecification": ReservationResourceSpecificationTypeDef,
        "UsagePrice": float,
    },
    total=False,
)

ListOfferingsResponseTypeDef = TypedDict(
    "ListOfferingsResponseTypeDef",
    {"NextToken": str, "Offerings": List[OfferingTypeDef]},
    total=False,
)

ReservationTypeDef = TypedDict(
    "ReservationTypeDef",
    {
        "Arn": str,
        "Count": int,
        "CurrencyCode": str,
        "Duration": int,
        "DurationUnits": Literal["MONTHS"],
        "End": str,
        "FixedPrice": float,
        "Name": str,
        "OfferingDescription": str,
        "OfferingId": str,
        "OfferingType": Literal["NO_UPFRONT"],
        "Region": str,
        "ReservationId": str,
        "ResourceSpecification": ReservationResourceSpecificationTypeDef,
        "Start": str,
        "State": Literal["ACTIVE", "EXPIRED", "CANCELED", "DELETED"],
        "Tags": Dict[str, str],
        "UsagePrice": float,
    },
    total=False,
)

ListReservationsResponseTypeDef = TypedDict(
    "ListReservationsResponseTypeDef",
    {"NextToken": str, "Reservations": List[ReservationTypeDef]},
    total=False,
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"Tags": Dict[str, str]}, total=False
)

MediaConnectFlowRequestTypeDef = TypedDict(
    "MediaConnectFlowRequestTypeDef", {"FlowArn": str}, total=False
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

PurchaseOfferingResponseTypeDef = TypedDict(
    "PurchaseOfferingResponseTypeDef", {"Reservation": ReservationTypeDef}, total=False
)

StartChannelResponseTypeDef = TypedDict(
    "StartChannelResponseTypeDef",
    {
        "Arn": str,
        "ChannelClass": Literal["STANDARD", "SINGLE_PIPELINE"],
        "Destinations": List[OutputDestinationTypeDef],
        "EgressEndpoints": List[ChannelEgressEndpointTypeDef],
        "EncoderSettings": EncoderSettingsTypeDef,
        "Id": str,
        "InputAttachments": List[InputAttachmentTypeDef],
        "InputSpecification": InputSpecificationTypeDef,
        "LogLevel": Literal["ERROR", "WARNING", "INFO", "DEBUG", "DISABLED"],
        "Name": str,
        "PipelineDetails": List[PipelineDetailTypeDef],
        "PipelinesRunningCount": int,
        "RoleArn": str,
        "State": Literal[
            "CREATING",
            "CREATE_FAILED",
            "IDLE",
            "STARTING",
            "RUNNING",
            "RECOVERING",
            "STOPPING",
            "DELETING",
            "DELETED",
            "UPDATING",
            "UPDATE_FAILED",
        ],
        "Tags": Dict[str, str],
    },
    total=False,
)

StartMultiplexResponseTypeDef = TypedDict(
    "StartMultiplexResponseTypeDef",
    {
        "Arn": str,
        "AvailabilityZones": List[str],
        "Destinations": List[MultiplexOutputDestinationTypeDef],
        "Id": str,
        "MultiplexSettings": MultiplexSettingsTypeDef,
        "Name": str,
        "PipelinesRunningCount": int,
        "ProgramCount": int,
        "State": Literal[
            "CREATING",
            "CREATE_FAILED",
            "IDLE",
            "STARTING",
            "RUNNING",
            "RECOVERING",
            "STOPPING",
            "DELETING",
            "DELETED",
        ],
        "Tags": Dict[str, str],
    },
    total=False,
)

StopChannelResponseTypeDef = TypedDict(
    "StopChannelResponseTypeDef",
    {
        "Arn": str,
        "ChannelClass": Literal["STANDARD", "SINGLE_PIPELINE"],
        "Destinations": List[OutputDestinationTypeDef],
        "EgressEndpoints": List[ChannelEgressEndpointTypeDef],
        "EncoderSettings": EncoderSettingsTypeDef,
        "Id": str,
        "InputAttachments": List[InputAttachmentTypeDef],
        "InputSpecification": InputSpecificationTypeDef,
        "LogLevel": Literal["ERROR", "WARNING", "INFO", "DEBUG", "DISABLED"],
        "Name": str,
        "PipelineDetails": List[PipelineDetailTypeDef],
        "PipelinesRunningCount": int,
        "RoleArn": str,
        "State": Literal[
            "CREATING",
            "CREATE_FAILED",
            "IDLE",
            "STARTING",
            "RUNNING",
            "RECOVERING",
            "STOPPING",
            "DELETING",
            "DELETED",
            "UPDATING",
            "UPDATE_FAILED",
        ],
        "Tags": Dict[str, str],
    },
    total=False,
)

StopMultiplexResponseTypeDef = TypedDict(
    "StopMultiplexResponseTypeDef",
    {
        "Arn": str,
        "AvailabilityZones": List[str],
        "Destinations": List[MultiplexOutputDestinationTypeDef],
        "Id": str,
        "MultiplexSettings": MultiplexSettingsTypeDef,
        "Name": str,
        "PipelinesRunningCount": int,
        "ProgramCount": int,
        "State": Literal[
            "CREATING",
            "CREATE_FAILED",
            "IDLE",
            "STARTING",
            "RUNNING",
            "RECOVERING",
            "STOPPING",
            "DELETING",
            "DELETED",
        ],
        "Tags": Dict[str, str],
    },
    total=False,
)

UpdateChannelClassResponseTypeDef = TypedDict(
    "UpdateChannelClassResponseTypeDef", {"Channel": ChannelTypeDef}, total=False
)

UpdateChannelResponseTypeDef = TypedDict(
    "UpdateChannelResponseTypeDef", {"Channel": ChannelTypeDef}, total=False
)

UpdateInputResponseTypeDef = TypedDict(
    "UpdateInputResponseTypeDef", {"Input": InputTypeDef}, total=False
)

UpdateInputSecurityGroupResponseTypeDef = TypedDict(
    "UpdateInputSecurityGroupResponseTypeDef",
    {"SecurityGroup": InputSecurityGroupTypeDef},
    total=False,
)

UpdateMultiplexProgramResponseTypeDef = TypedDict(
    "UpdateMultiplexProgramResponseTypeDef",
    {"MultiplexProgram": MultiplexProgramTypeDef},
    total=False,
)

UpdateMultiplexResponseTypeDef = TypedDict(
    "UpdateMultiplexResponseTypeDef", {"Multiplex": MultiplexTypeDef}, total=False
)

UpdateReservationResponseTypeDef = TypedDict(
    "UpdateReservationResponseTypeDef", {"Reservation": ReservationTypeDef}, total=False
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef", {"Delay": int, "MaxAttempts": int}, total=False
)
