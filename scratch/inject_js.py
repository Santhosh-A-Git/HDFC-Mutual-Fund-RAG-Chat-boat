# pyrefly: ignore [missing-import]
from bs4 import BeautifulSoup

def process_html():
    with open('src/ui/static/index.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        
    # 1. Add ID to the chat scroll container
    chat_container = soup.find('div', class_=lambda c: c and 'chat-scroll' in c)
    chat_container['id'] = 'chat-container'
    
    # 2. Add ID to form and input
    form = soup.find('form')
    form['id'] = 'chat-form'
    
    input_field = form.find('input')
    input_field['id'] = 'chat-input'
    
    # 3. Add ID to suggestion chips
    buttons = chat_container.find_all('button')
    for btn in buttons:
        btn['class'] = btn.get('class', []) + ['suggestion-chip']
        
    # 4. Remove dummy messages (User Message, Bot Response, Thinking State)
    # The first child is the welcome message. The rest are mocks.
    children = chat_container.find_all('div', recursive=False)
    if len(children) > 1:
        for child in children[1:]:
            child.decompose()
            
    # 5. Inject JavaScript
    script_tag = soup.new_tag('script')
    script_tag.string = """
    document.addEventListener('DOMContentLoaded', () => {
        const form = document.getElementById('chat-form');
        const input = document.getElementById('chat-input');
        const chatContainer = document.getElementById('chat-container');
        const chips = document.querySelectorAll('.suggestion-chip');
        
        // Helper to scroll to bottom
        const scrollToBottom = () => {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        };
        
        // Handle Suggestion Chips
        chips.forEach(chip => {
            chip.addEventListener('click', (e) => {
                e.preventDefault();
                let text = chip.innerText.replace('Will be rejected - Advisory', '').trim();
                input.value = text;
                form.dispatchEvent(new Event('submit'));
            });
        });

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const query = input.value.trim();
            if(!query) return;
            
            // Clear input
            input.value = '';
            
            // 1. Append User Message
            const userMsgHTML = `
            <div class="flex items-end gap-sm self-end max-w-[85%] mt-sm">
                <div class="bg-primary-container p-sm md:p-md rounded-2xl rounded-br-sm text-on-primary-container font-body-sm text-body-sm shadow-md bg-gradient-to-b from-[#3B82F6] to-[#2563EB] shadow-inner leading-relaxed">
                    <p>${query}</p>
                </div>
                <div class="w-8 h-8 rounded-full bg-surface-container flex items-center justify-center shrink-0 border border-white/10 overflow-hidden">
                    <span class="material-symbols-outlined text-white text-[18px]">person</span>
                </div>
            </div>`;
            chatContainer.insertAdjacentHTML('beforeend', userMsgHTML);
            scrollToBottom();
            
            // 2. Append Thinking State
            const thinkingId = 'thinking-' + Date.now();
            const thinkingHTML = `
            <div id="${thinkingId}" class="flex items-start gap-sm self-start max-w-[85%] mt-sm">
                <div class="w-8 h-8 rounded-full bg-surface-container flex items-center justify-center shrink-0 border border-white/10">
                    <span class="material-symbols-outlined text-primary text-[18px]">smart_toy</span>
                </div>
                <div class="glass-panel px-md py-sm rounded-2xl rounded-bl-sm shadow-sm border border-white/10 flex items-center gap-1 h-[42px]">
                    <div class="w-1.5 h-1.5 bg-primary rounded-full dot-pulse"></div>
                    <div class="w-1.5 h-1.5 bg-primary rounded-full dot-pulse"></div>
                    <div class="w-1.5 h-1.5 bg-primary rounded-full dot-pulse"></div>
                </div>
            </div>`;
            chatContainer.insertAdjacentHTML('beforeend', thinkingHTML);
            scrollToBottom();
            
            // 3. Fetch API
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query })
                });
                const data = await response.json();
                
                // Remove thinking state
                document.getElementById(thinkingId).remove();
                
                // Format Markdown response (very basic formatting for blockquotes and bold)
                let formattedResponse = data.response
                    .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>')
                    .replace(/> "(.*?)"/g, '<blockquote class="border-l-2 border-primary/50 pl-sm py-1 my-sm bg-surface-container-lowest/50 rounded-r-md border-l-4 bg-surface-container-lowest/80"><p class="text-[11px] text-outline">$1</p></blockquote>');
                
                // 4. Append Bot Message
                const botMsgHTML = `
                <div class="flex items-start gap-sm self-start max-w-[85%] mt-sm">
                    <div class="w-8 h-8 rounded-full bg-surface-container flex items-center justify-center shrink-0 border border-white/10">
                        <span class="material-symbols-outlined text-primary text-[18px]">smart_toy</span>
                    </div>
                    <div class="glass-panel p-sm md:p-md rounded-2xl rounded-bl-sm text-on-surface-variant font-body-sm text-body-sm shadow-sm border border-white/10 space-y-sm">
                        <p style="white-space: pre-wrap;">${formattedResponse}</p>
                    </div>
                </div>`;
                chatContainer.insertAdjacentHTML('beforeend', botMsgHTML);
                scrollToBottom();
                
            } catch (err) {
                document.getElementById(thinkingId).remove();
                alert("Error connecting to server.");
            }
        });
    });
    """
    soup.body.append(script_tag)
    
    with open('src/ui/static/index.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("Injected JS and cleaned DOM.")

if __name__ == '__main__':
    process_html()
