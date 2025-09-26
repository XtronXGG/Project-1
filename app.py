import streamlit as st
import hashlib
from datetime import datetime

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash_value):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash_value

class Blockchain:
    def __init__(self):
        self.chain = [self._create_genesis_block()]

    def _create_genesis_block(self):
        genesis_timestamp = datetime.now()
        genesis_hash = self._calculate_hash(0, '0', genesis_timestamp, 'Genesis Block')
        return Block(0, '0', genesis_timestamp, 'Genesis Block', genesis_hash)

    def _calculate_hash(self, index, previous_hash, timestamp, data):
        value = f"{index}{previous_hash}{timestamp}{data}"
        return hashlib.sha256(value.encode('utf-8')).hexdigest()

    def add_block(self, data):
        previous_block = self.chain[-1]
        new_index = previous_block.index + 1
        new_timestamp = datetime.now()
        new_hash = self._calculate_hash(new_index, previous_block.hash, new_timestamp, data)
        new_block = Block(new_index, previous_block.hash, new_timestamp, data, new_hash)
        self.chain.append(new_block)

# Initialize blockchain
if "blockchain" not in st.session_state:
    st.session_state.blockchain = Blockchain()

st.title("📒 Blockchain-based Digital Diary")

entry = st.text_area("Write your diary entry:", key="entry")
if st.button("Add Entry"):
    if entry.strip():
        st.session_state.blockchain.add_block(entry)
        st.success("Entry added successfully!")
        # Clear the text area after adding
        st.session_state.entry = ""  # Note: Streamlit will re-run, so use session_state for clearing if needed
        st.rerun()  # Rerun to update the display immediately

st.subheader("📜 Diary Timeline")
for i, block in enumerate(st.session_state.blockchain.chain):
    # Format timestamp for better display
    formatted_timestamp = block.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f"""
    **Index:** {block.index}  
    **Timestamp:** {formatted_timestamp}  
    **Entry:** {block.data}  
    **Hash:** `{block.hash}`  
    **Previous Hash:** `{block.previous_hash}`  
    """)
    if i < len(st.session_state.blockchain.chain) - 1:  # Avoid extra separator after last block
        st.write("---")
