import { GoogleGenAI, Chat } from "@google/genai";

const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });

export const createChatSession = (): Chat => {
  return ai.chats.create({
    model: 'gemini-3-flash-preview',
    config: {
      systemInstruction: `You are the AI Assistant for Sahwan Law, a prestigious law firm in Bahrain established in 1975. 
      Your tone should be professional, empathetic, and concise.
      You can provide general information about:
      - Corporate Law (Formation, M&A)
      - Litigation (Civil, Commercial, Arbitration)
      - Notarization
      - Real Estate
      - Banking & Finance
      
      Do not give specific legal advice on active cases. Instead, encourage the user to book a consultation using the form on the website or call +973 17 531 566.
      Always format your responses nicely.`,
    },
  });
};

export const sendMessageStream = async (chat: Chat, message: string) => {
  return await chat.sendMessageStream({ message });
};