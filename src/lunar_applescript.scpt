tell application "System Events"
    -- Try to find Lunar in the menu bar extras
    set menuExtras to menu bar items of menu bar 1 of application process "SystemUIServer"
    
    set lunarFound to false
    repeat with menuExtra in menuExtras
        try
            set menuName to description of menuExtra
            log "Menu extra: " & menuName
            
            if menuName contains "Lunar" then
                log "Found Lunar menu extra: " & menuName
                set lunarFound to true
                
                -- Click the menu extra to open its menu
                click menuExtra
                delay 0.5
                
                -- Try to find content in the menu
                try
                    set menuItems to menu items of menu 1 of menuExtra
                    log "Menu items count: " & (count of menuItems)
                    
                    repeat with menuItem in menuItems
                        try
                            set menuItemName to name of menuItem
                            log "Menu item: " & menuItemName
                            
                            -- If we find an HP monitor entry, try to interact with it
                            if menuItemName contains "HP" then
                                log "Found HP monitor item: " & menuItemName
                                -- Click on it to see sliders
                                -- click menuItem
                                -- delay 0.5
                            end if
                        end try
                    end repeat
                on error errMsg
                    log "Error getting menu items: " & errMsg
                end try
                
                -- Close the menu
                click menuExtra
            end if
        end try
    end repeat
    
    if not lunarFound then
        log "Lunar menu extra not found"
    end if
end tell 