const { SlashCommandBuilder } = require('discord.js');
const { request } = require('undici');

module.exports = {
    cooldown: 5,
    data: new SlashCommandBuilder()
        .setName('martingpt')
        .setDescription('Replies using martingpt')
		.addStringOption(option =>
			option
				.setName('prompt')
				.setDescription('Message to prompt MartinGPT')
				.setRequired(true)),
    async execute(interaction) {
        const { commandName } = interaction;
        await interaction.deferReply();
    
        if (commandName === 'martingpt') {
			const promptText = interaction.options.getString('prompt')
			// const promptText = 'what games do you play?';
			console.log(promptText);

            try {
                // Assuming `content` should be taken from user input or predefined
                const content = "some content to send"; // Replace or modify as needed
                const response = await request(process.env.API_ENDPOINT, {
                    method: "POST",
                    headers: {
                        authorization: `Bot ${process.env.TOKEN}`,
                        "content-type": "application/json"
                    },
                    body: JSON.stringify({ text: promptText }) // Correctly stringify the JSON body
                });

				if (response.statusCode === 200) {
					const data = await response.body.json(); // Parse the JSON response only once
					
					console.log("API Response:", data); // Log the data for debugging purposes
					
					if (!data || !data.response) {
						console.error("Empty or undefined data received from API.");
						await interaction.editReply("Error: No content received from API.");
					} else {
						await interaction.editReply(`${interaction.user}: ${promptText}  \n\nMartinGPT: ${data.response}`);
					}
				} else {
					throw new Error(`API responded with status code: ${response.statusCode}`);
				}
            } catch (error) {
                console.error('Failed to fetch data from martingpt API:', error);
                await interaction.editReply({ content: 'Failed to process your request.' });
            }
        }
    },
};
