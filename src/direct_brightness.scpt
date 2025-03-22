tell application "System Events"
    -- Make sure MonitorControl is running
    if not (exists process "MonitorControl") then
        return "MonitorControl is not running"
    end if
    
    tell process "MonitorControl"
        -- Get the menu bar item
        set menuBarItem to menu bar item 1 of menu bar 1
        
        -- Click to show menu
        click menuBarItem
        delay 1
        
        -- Try to get window position
        try
            set win to window 1
            set winPos to position of win
            set winSize to size of win
            
            log "Window position: " & winPos
            log "Window size: " & winSize
            
            -- Try clicking and dragging in the window
            set baseX to (item 1 of winPos)
            set baseY to (item 2 of winPos)
            
            -- Click near the top of the window
            click at {baseX + 50, baseY + 30}
            delay 0.5
            
            -- Try dragging the slider
            drag from {baseX + 20, baseY + 30} to {baseX + 100, baseY + 30}
            
        on error errMsg
            log "Error interacting with window: " & errMsg
        end try
        
        delay 0.5
        
        -- Close menu
        click menuBarItem
        
        -- Try to access menu items
        try
            -- Get the menu
            set mcMenu to menu 1 of mcItem
            
            -- Get all menu items
            set menuItems to menu items of mcMenu
            log "Found " & (count of menuItems) & " menu items"
            
            -- Look for the HP monitor section
            repeat with i from 1 to count of menuItems
                set currentItem to item i of menuItems
                try
                    log "Menu item " & i & ": " & name of currentItem
                    
                    -- If this is a menu item with submenus, check those too
                    if exists (menu 1 of currentItem) then
                        set subMenu to menu 1 of currentItem
                        set subItems to menu items of subMenu
                        log "Submenu items: " & (count of subItems)
                        
                        repeat with j from 1 to count of subItems
                            set subItem to item j of subItems
                            log "Submenu item " & j & ": " & name of subItem
                        end repeat
                    end if
                end try
            end repeat
            
        on error errMsg
            log "Error accessing menu: " & errMsg
        end try
        
        delay 0.5
        
        -- Close menu
        click mcItem
    end tell
end tell

tell application "System Events"
    tell process "MonitorControl"
        -- Click the menu bar item to show the menu
        click menu bar item 1 of menu bar 1
        delay 1
        
        -- Try to access the UI elements in different ways
        try
            -- Method 1: Try to get all UI elements
            set allElements to UI elements of front window
            log "Number of UI elements found: " & (count of allElements)
            
            -- Method 2: Try to get all groups
            set allGroups to groups of front window
            log "Number of groups found: " & (count of allGroups)
            
            -- Method 3: Try to get all sliders directly
            set allSliders to sliders of front window
            log "Number of sliders found: " & (count of allSliders)
            
            -- Log details of each UI element
            repeat with elem in allElements
                try
                    log "Element: " & (class of elem as string)
                    log "Role: " & (role of elem as string)
                    log "Description: " & (description of elem as string)
                end try
            end repeat
            
        on error errMsg
            log "Error accessing elements: " & errMsg
        end try
        
        delay 0.5
        
        -- Close the menu
        click menu bar item 1 of menu bar 1
    end tell
end tell 