import streamlit as st
import hashlib
import json

def generate_cache_key(*args, **kwargs):
    key_data = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True)
    return hashlib.md5(key_data.encode()).hexdigest()

def cached_api_call(api_func, *args, **kwargs):
    cache_key = generate_cache_key(api_func.__name__, *args, **kwargs)
    if cache_key in st.session_state:
        return st.session_state[cache_key]
    result = api_func(*args, **kwargs)
    st.session_state[cache_key] = result
    return result
