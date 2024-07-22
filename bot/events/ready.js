const { Events } = require('discord.js');

module.exports = {
    name: Events.ClientReady,
    once: true,
    execute(client) {
        console.log(`'Ready! Loggd in as ${client.user.tag}`);
    },
};