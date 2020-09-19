constructor(){
  super({
    // whether to reload the browser window when enabled or disabled;
    // it's always better when a plugin can be toggled without reloading,
    // but the option is available if needed (default: false)
    requiresPageReload: false
  });
}

enabled(){
  // executed immediately after constructor if the plugin is enabled,
  // or later if the plugin is enabled manually

  // only the <head> tag and the main .js-app elements are guaranteed to exist

  // load configuration, define variables and functions,
  // create custom styles, modify {{mustache}} templates
}

ready(){
  // executed once the app layout is generated,
  // or immediately after enabled() if the plugin is enabled manually later

  // the TweetDeck accounts, settings, and column list are available
  // most of the website layout is generated, but column contents are still loading

  // add event listeners, modify the sidebar,
  // inject your code into TweetDeck functions
}

configure(){
  // if present, the plugin will have a 'Configure' button which calls this method

  // if used alongside the 'configfile' meta tag, this method will take precedence
  // over the default behavior of opening Windows Explorer
}

disabled(){
  // executed when the plugin is manually disabled
  // omit if you set 'requiresPageReload' to true

  // remove custom elements and event listeners,
  // revert {{mustache}} templates and injected functions
}