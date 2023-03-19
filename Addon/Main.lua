local _G = _G
local _, QueueTdb = ...
local phoneNumber

local QueueT = CreateFrame("Frame", "ATT", UIParent)
local panels = {}
local panelMeta = {}

for funcName in pairs(panelMeta) do
    for panel in pairs(panels) do
        panel[funcName] = nil
    end
    panelMeta[funcName] = nil
end

local function CreateEditBox(name, parent, height, width)
    local editbox = CreateFrame("EditBox", parent:GetName() .. name, parent, "InputBoxTemplate")
    editbox:SetHeight(height)
    editbox:SetWidth(width)
    editbox:SetAutoFocus(false)
    editbox:SetMaxLetters(15)
    local label = editbox:CreateFontString(nil, "BACKGROUND", "GameFontNormal")
    label:SetText(name)
    label:SetPoint("BOTTOMLEFT", editbox, "TOPLEFT", -3, 0)
    return editbox
end

local function QueueT_OnLoad(self)
    -- self:RegisterEvent("PLAYER_ENTERING_WORLD")
    -- https://wowpedia.fandom.com/wiki/Saving_variables_between_game_sessions
    phoneNumber = PHONENUMBER or QueueTdb.PhoneNumber
    self:SetScript("OnEvent", function(self, event, ...)
        if self[event] then
            self[event](self, ...)
        end
    end);
    print("1")
    self:CreateOptions()
    print("Created Options")
end

function QueueT:CreateOptions()
    print("2")
    local panel = self.AddOptionsPanel("QueueT", function()
    end)
    self.panel = panel
    AddSlashCommand("QueueT", "/queueT")
    print("6")
    local title, subText = panel:MakeTitleTextAndSubText("QueueT - Receive Texts when your Queue POPs!")
    self:InputPhoneNumber()
    print("5")
end

function QueueT:InputPhoneNumber()
    print("3")
    local panel = self.panel
    local btns = {}
    self.btns = btns
    local phoneNumberEditBox = CreateEditBox("Phone Number", panel, 30, 100)
    print(phoneNumber)
    phoneNumberEditBox:SetText(phoneNumber)
    local saveButton = panel:MakeButton('name', 'Save', 'newsize', 2, 'description', "Save Phone Number",
        'func',
        function()
            local phoneNumberValue = phoneNumberEditBox:GetText()
            -- local isPhoneNumberGood = match(phoneNumber, "^[0-9]{10}$");
            -- print(isPhoneNumberGood)
            if phoneNumberValue then
                phoneNumber = phoneNumberValue
                -- persist to WTF\Account\ACCOUNTNAME\SavedVariables\AddOnName.lua
                PHONENUMBER = phoneNumber
                print("Updated Phone # to: |cffFF4500" .. phoneNumberValue)
            end
        end
    )
    phoneNumberEditBox:SetPoint("TOPLEFT", panel, "TOPLEFT", 5, -65)
    saveButton:SetPoint("TOPLEFT", phoneNumberEditBox, "BOTTOMLEFT", -5, -5)
    print("4")
end

function AddSlashCommand(name, ...)
    local num = 0
    local name_upper = name:upper()
    for i = 1, select('#', ...) do
        local cmd = select(i, ...)
        num = num + 1
        _G["SLASH_" .. name_upper .. num] = cmd
        local cmd_lower = cmd:lower()
        if cmd_lower ~= cmd then
            num = num + 1
            _G["SLASH_" .. name_upper .. num] = cmd_lower
        end
    end
    _G.hash_SlashCmdList[name_upper] = nil
    _G.SlashCmdList[name_upper] = function()
        InterfaceOptionsFrame_OpenToCategory(name)
    end
end

function panelMeta:MakeTitleTextAndSubText(titleText, subTextText)
    local title = self:CreateFontString(nil, "ARTWORK", "GameFontNormalLarge")
    title:SetText(titleText)
    title:SetJustifyH("LEFT")
    title:SetJustifyV("TOP")
    title:SetPoint("TOPLEFT", 16, -16)

    local subText = self:CreateFontString(nil, "ARTWORK", "GameFontNormal")
    subText:SetText(subTextText)
    subText:SetNonSpaceWrap(true)
    subText:SetJustifyH("LEFT")
    subText:SetJustifyV("TOP")
    subText:SetPoint("TOPLEFT", title, "BOTTOMLEFT", 0, -8)
    subText:SetPoint("RIGHT", -32, 0)

    return title, subText
end

local function generic_OnEnter(self)
end

local function generic_OnLeave(self)
end

local getArgs, doneArgs
do
    local tmp = {}
    function getArgs(...)
        assert(next(tmp) == nil)
        for i = 1, select('#', ...), 2 do
            local k, v = select(i, ...)
            if type(k) ~= "string" then
                error(("Received a bad key, must be a %q, got %q (%s)"):format("string", type(k), tostring(k)), 3)
            elseif tmp[k] ~= nil then
                error(("Received key %q twice"):format(k), 3)
            end
            tmp[k] = v
        end
        return tmp
    end

    function doneArgs(args)
        assert(args == tmp)
        for k in pairs(args) do
            args[k] = nil
        end
        return nil
    end
end

do
    local function donothing()
    end

    local function button_OnClick(self)
        self.clickFunc()
    end

    function panelMeta:MakeButton(...)
        local args = getArgs(...)

        local name
        local i = 0
        repeat
            i = i + 1
            name = self:GetName() .. "_Button" .. i
        until not _G[name]

        local button = CreateFrame("Button", name, args.extra or self, "UIPanelButtonTemplate")

        self.controls[button] = true
        button:SetText(args.name)
        button.tooltipText = args.description
        if args.newsize == 1 then
            button:SetSize(80, 30);
        elseif args.newsize == 2 then
            button:SetSize(65, 30);
        else
            button:SetSize(90, 30);
        end
        button.SetValue = donothing
        button.clickFunc = args.func
        button:SetScript("OnClick", button_OnClick)
        button:SetScript("OnEnter", generic_OnEnter)
        button:SetScript("OnLeave", generic_OnLeave)
        args = doneArgs(args)
        return button
    end
end



do
    local function makePanel(name, parentName, controlCreationFunc)
        local panel
        if not parentName then
            panel = CreateFrame("Frame", name .. "_Panel")
        else
            panel = CreateFrame("Frame", parentName .. "_Panel_" .. name)
        end
        panels[panel] = true

        panel.name = name
        panel.controls = {}
        panel.parent = parentName

        panel.okay = panel_okay
        panel.cancel = panel_cancel
        panel.default = panel_default

        InterfaceOptions_AddCategory(panel)

        panel.controlCreationFunc = controlCreationFunc
        panel:SetScript("OnShow", panel_OnShow)
        for k, v in pairs(panelMeta) do
            panel[k] = v
        end

        return panel
    end
    function QueueT.AddOptionsPanel(name, controlCreationFunc)
        return makePanel(name, nil, controlCreationFunc)
    end
end

QueueT:RegisterEvent("ADDON_LOADED")
QueueT:SetScript("OnEvent", QueueT_OnLoad)
