import math

import av
import matplotlib.pyplot as plt
import streamlit as st
import streamlit_nested_layout
from streamlit.components.v1 import html
from streamlit_webrtc import webrtc_streamer

from visualize import JankoHrasko


def move_fwd():
    print('Move FWD')


def move_bwd():
    print('Move BWD')


def move_left():
    print('Move LEFT')


def move_right():
    print('Move RIGHT')


def video_callback(frame):
    img = frame.to_ndarray(format='bgr24')
    return av.VideoFrame.from_ndarray(img, format='bgr24')


st.set_page_config(layout='wide')
st.title('Janko Hraško Controller')

col_1, col_2, col_3 = st.columns(3)

with col_1:
    st.subheader('Effector position')

    if 'effector_coords' not in st.session_state:
        st.session_state['effector_coords'] = (0, 0, 0)

    slider_x = st.slider('X')
    slider_y = st.slider('Y')
    slider_z = st.slider('Z')

    col_b1, col_b2 = st.columns(2)

    with col_b1:
        submit = st.button('Execute')

        if submit:
            st.session_state['effector_coords'] = (slider_x, slider_y, slider_z)
            send_coords()

    with col_b2:
        btn_container = st.empty()
        grab = btn_container.button('Grab', on_click=grip)

        if grab:
            btn_container.empty()
            grab = btn_container.button('Release', on_click=release)

    with st.expander('Precise control'):
        with st.form(key='effector'):
            coord_x = st.number_input(
                'X',
                value=slider_x
            )
            coord_y = st.number_input(
                'Y',
                value=slider_y
            )
            coord_z = st.number_input(
                'Z',
                value=slider_z
            )

            submit = st.form_submit_button(label='Execute')

            if submit:
                st.session_state['effector_coords'] = (coord_x, coord_y, coord_z)
                send_coords()

    st.subheader('Base movement')

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)

    with col_m1:
        st.button('🠕', on_click=move_fwd)
    with col_m2:
        st.button('🠗', on_click=move_bwd)
    with col_m3:
        st.button('🠔', on_click=move_left)
    with col_m4:
        st.button('🠖', on_click=move_right)

    html(
        """
        <script>
        const doc = window.parent.document;
        buttons = Array.from(doc.querySelectorAll('button[kind=secondary]'));
        
        const fwd_btn = buttons.find(el => el.innerText === '🠕');
        const bwd_btn = buttons.find(el => el.innerText === '🠗');
        const left_btn = buttons.find(el => el.innerText === '🠔');
        const right_btn = buttons.find(el => el.innerText === '🠖');
        
        doc.addEventListener('keydown', function(e) {
            switch (e.code) {
                case 'ArrowUp':
                    fwd_btn.click();
                    break;
                case 'ArrowDown':
                    bwd_btn.click();
                    break;
                case 'ArrowLeft':
                    left_btn.click();
                    break;
                case 'ArrowRight':
                    right_btn.click();
                    break;
            }
        });
        </script>
        """,
        height=0,
        width=0,
    )

deg = math.pi / 180

if 'robot' not in st.session_state:
    st.session_state['robot'] = JankoHrasko()

if 'joint_config' not in st.session_state:
    st.session_state['joint_config'] = [0 * deg, 0 * deg, 0 * deg, 45 * deg, 45 * deg, 0 * deg]
    st.session_state['robot'].plot(
        q=st.session_state['joint_config'],
        backend='pyplot',
        block=False,
        jointaxes=True,
        eeframe=True,
        shadow=False
    )
    st.session_state['arm_fig'] = plt.gcf()

q = [0 * deg, 0 * deg, 0 * deg, 45 * deg, 45 * deg, 0 * deg]

if q != st.session_state['joint_config']:
    st.session_state['joint_config'] = q

    st.session_state['robot'].plot(
        q=st.session_state['joint_config'],
        backend='pyplot',
        block=False,
        jointaxes=True,
        eeframe=True,
        shadow=False
    )
    st.session_state['arm_fig'] = plt.gcf()

with col_2:
    st.subheader('Arm position')
    st.pyplot(st.session_state['arm_fig'])

with col_3:
    st.subheader('Camera')
    webrtc_streamer(key='camera', video_frame_callback=video_callback)
