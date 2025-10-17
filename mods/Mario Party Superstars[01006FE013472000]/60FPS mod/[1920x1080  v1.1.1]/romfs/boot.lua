print "-----------------------------------------------------"
print "- boot.lua ------------------------------------------"
print "-----------------------------------------------------"

local engine = require 'BezelEngineInitializer'
local GameControllerStyle = require 'BezelEnum.GameControllerStyle'

engine:SetDefaultCulture("jaJP")

local GpuHeapType = require 'BezelEnum.GpuHeapType'
local GpuMemoryProperty = require 'BezelEnum.GpuMemoryProperty'

--engine:SetGpuHeapSize(GpuHeapType.Resident, GpuMemoryProperty.CpuInvisibleGpuCachedCompressible, 512 * 1024 * 1024)
--engine:SetGpuHeapSize(GpuHeapType.Resident, GpuMemoryProperty.CpuUncachedGpuCached, 512 * 1024 * 1024)
--engine:SetGpuHeapSize(GpuHeapType.Temporal, GpuMemoryProperty.CpuUncachedGpuCached, 512 * 1024 * 1024)
engine:SetGpuHeapSize(GpuHeapType.Resident, GpuMemoryProperty.CpuInvisibleGpuCachedCompressible, 128 * 1024 * 1024)
engine:SetGpuHeapSize(GpuHeapType.Resident, GpuMemoryProperty.CpuUncachedGpuCached, 64 * 1024 * 1024)
engine:SetGpuHeapSize(GpuHeapType.Temporal, GpuMemoryProperty.CpuUncachedGpuCached, 3072 * 1024 * 1024)

engine:SetSamplerDescriptorSlotCount(256)
engine:SetTextureViewDescriptorSlotCount(4096)

engine:SetNumberOfGameControllerPlayers(1, 1)
engine:SetAutoStartControllerSupportAppletEnabled(true)
engine:SetGameControllerStyle(GameControllerStyle.Classic)

engine:SetStartupUserAccountEnabled(true)
local RenderingResolutionStage = require 'BezelEnum.RenderingResolutionStage'
engine:SetBaseResolution(1920, 1080)
engine:SetRenderingResolutionOnBoostMode(1920, 1080)
engine:SetMaxRenderingResolution(3840, 2160)
engine:SetRenderingResolutionOnNormalMode(RenderingResolutionStage.Stage0, 1152, 648)
engine:SetRenderingResolutionOnNormalMode(RenderingResolutionStage.Stage1, 1280, 720)
engine:SetRenderingResolutionOnBoostMode(RenderingResolutionStage.Stage0, 1600, 900)
engine:SetRenderingResolutionOnBoostMode(RenderingResolutionStage.Stage1, 1920, 1080)
engine:SetDefaultToolViewModeEnabled(false)
engine:SetBuiltInRenderSystemEnabled(false)
engine:SetParticleFx2ViewerEnabled(true)
engine:SetLayoutConstantBufSize(1024 * 1024 * 4)
--engine:SetPcWindowSize(1920, 1080)

--Fxtriggerパラメータ Nd榎並
engine:SetFxTriggerAudioCount(64*8)
engine:SetFxTriggerAnimEventPlayerCount(64 * 3)
engine:SetFxTriggerAnimEventCount(128 * 3)
engine:SetFxTriggerAnimEventTriggerCount(256 * 2)
engine:SetFxTriggerActorParameterBufferSize(512 * 1024 * 16)
engine:SetFxTriggerVibrationCount(32 * 8)
engine:SetFxTriggerfxTriggerIsTriggerUpdateCallbackEnabled(true)
engine:SetFxTriggerActorCount(128 * 2)

-- 物理設定
engine:SetPhysicsWorldCount(2) -- 0: デフォルト, 1: キャラクターの揺れもの等、ゲームロジックに関わらない装飾

-- サウンドヒープサイズ設定
engine:SetAudioHeapSize(160 * 1024 * 1024) -- デフォルト値 50 * 1024 * 1024 (50MB)

engine:Initialize()

print "<<<< Engine Initialized! >>>>"
