# https://twitter.com/m0ham3dxx

# Handy fish script for webdev testing - pnpm method
# NextJs 13 + Tailwindcss-Animated + Tailwind prettier plugin + daisyui 
# Copy the fish script in ~/.config/fish/functions/
# Tested on LINUX ONLY

function wdv
    clear
    echo ""
    echo ""
    echo ""
    echo "************************************"
    echo ""
    echo (set_color FF55BB)"This function executes the following commmands"
    echo ""
    echo (set_color 16FF00)" A> pnpm dlx create-next-app@latest"
    echo (set_color 16FF00)" B> pnpm i -D prettier prettier-plugin-tailwindcss"
    echo (set_color 16FF00)" C> pnpm i tailwindcss-animated"
    echo (set_color 16FF00)" D> pnpm i -D daisyui@latest"
    echo ""
    echo ""
    echo (set_color B3FFAE)"++++++++++++++++++++++++++++++++++++"
    echo ""
    echo ""
    echo "Set Directory for setup (NO SPACES ALLOWED !): "
    echo ""
    echo ""
    echo (set_color B3FFAE) "++++++++++++++++++++++++++++++++++++"
    echo ""
    read -l dir 
    echo ""
    echo (set_color FF1E1E) "Installation in the following directory :-" $dir
    echo ""
    echo "Press any key to start..."
    read -l
    echo (set_color FF6D28)""
    echo (set_color FF6D28)""
    echo (set_color FF6D28)""
    echo (set_color FF6D28)"=> STARTING... A> pnpm dlx create-next-app@latest "
    pnpm dlx create-next-app@latest $dir
    echo (set_color FF6D28)"DONE! - DONE!- DONE! - DONE!"
    echo (set_color FF6D28)""
    echo (set_color FF6D28)""
    echo (set_color FF6D28)" Changin Directory..."
    cd $dir && ls -al 
    echo (set_color F637EC)"=> STARTING....B>pnpm i -D prettier prettier-plugin-tailwindcss"
    pnpm i -D prettier prettier-plugin-tailwindcss 
    echo (set_color F637EC)"DONE! - DONE!- DONE! - DONE!"
    echo (set_color F637EC)""
    echo (set_color F637EC)""
    echo (set_color 94B3FD)"=> STARTING... C> pnpm i tailwindcss-animated"
    pnpm i tailwindcss-animated 
    echo (set_color 94B3FD)"DONE! - DONE!- DONE! - DONE!"
    echo ""
    echo ""
    echo (set_color B983FF)"=> Starting...pnpm i -D daisyui@latest"
    pnpm i -D daisyui@latest
    echo (set_color B983FF)"DONE! - DONE!- DONE! - DONE!"
    echo ""
    echo " ALL INSTALLATIONS SUCCESSFUL"
    cat -n package.json
    ls -al 
    pnpm run dev --turbo
end
