---
title: A Path Toward Finding Schrödinger’s Equation
date: 2025-11-07
image: img/ChatGPT-Image-Nov-7-2025-02_09_53-PM.webp
excerpt: If there’s one equation you want to know to impress people at a dinner party, it’s the crown jewel of quantum physics: Schrödinger’s equation. Perhaps because of its mystical, counterintuitive aura, quantum physics enjoys a reputation for being incomprehensible to mere mortals. In my view, that reputation is totally undeserved. Other branches of physics use …
format: html
---

<p>If there’s one equation you want to know to impress people at a dinner party, it’s the crown jewel of quantum physics: Schrödinger’s equation. Perhaps because of its mystical, counterintuitive aura, quantum physics enjoys a reputation for being incomprehensible to mere mortals. In my view, that reputation is totally undeserved. Other branches of physics use equations that may be less famous but are often far more difficult to grasp (that will be the topic of another post). Still, this mysterious image persists in popular culture, where countless pseudo-gurus invoke “quantum phenomena” to justify their scams.</p>

<p>In a less dramatic way, Schrödinger’s equation also appears on our screens — as shorthand for “mathematical complexity.” From the science-fiction film <em>Arrival</em>, where it accompanies the deciphering of an alien language, to the children’s animated film <em>My Little Pony</em>, where it pops up humorously (see image below), this equation has become a cultural symbol of deep science.</p>

<figure>
  <img src="img/SchrodingerInMovies.webp" 
       alt="Wave–particle duality illustration with Schrödinger’s cat" 
       />
  <figcaption>
    The Schrödinger’s equation in movies: according to Denis Villeneuve, this could help us decipher an alien language.
  </figcaption>
</figure>

<p>But what is it really? Do you truly need a PhD in mathematics to understand where it comes from? Not at all. As we’ll see, with just a few lines of simple algebra (first-year university level), the equation practically reveals itself.</p>

<p>The only real challenge lies in the physicist’s idea of drawing an analogy between light and matter — between wave and particle. This wave-particle duality emerged in the early 1900s from the work of Albert Einstein, Max Planck, and Louis de Broglie (all three would later win the Nobel Prize in Physics). From their ideas came the fundamental relations of Planck–Einstein and de Broglie:</p>

<ul>
  <li>\( E = \hbar \,\omega \)</li> (i.e. the photon energy is proportional to the photon frequency, \(\hbar\) is the reduced Planck constant)
  <li>\( \vec{p} = \hbar \,\vec{k} \)</li> (i.e. the particle momentum is proportional to the wave vector)
</ul>

<p>Back in high school, everyone learns that for matter, energy and motion are linked by \( E = \frac{1}{2} m v^{2} \), which can also be written as \( E = \frac{p^{2}}{2m} \), where \( \vec{p} = m\,\vec{v} \) is the momentum.</p>

<p>Similarly, for waves, the classic dispersion relation is \( \omega = c\,k \), which connects the frequency \( \omega \) to the wave vector \( \vec{k} \).</p>

<p>By dividing the first equation by \( \hbar \) and multiplying the second by that same \( \hbar \), we obtain the desired analogy (using the Planck–Einstein and de Broglie relations given above):</p>

<div class="tbl"><table>
  <thead>
    <tr>
      <th></th>
      <th>Light</th>
      <th>Matter</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Particle-like</strong></td>
      <td>\( E = p\,c \)</td>
      <td>\( E = \frac{p^{2}}{2m} \)</td>
    </tr>
    <tr>
      <td><strong>Wave-like</strong></td>
      <td>\( \omega = c\,k \)</td>
      <td>\( \omega = \frac{\hbar\,k^{2}}{2m} \)</td>
    </tr>
  </tbody>
</table></div>

<p>Now, a plane progressive wave can be written as:</p>

$$
\psi(\vec r,t)=\psi_{0}\,e^{\,i(\vec k\cdot \vec r-\omega t)} ,
\qquad \text{with}\quad \omega=\frac{\hbar k^{2}}{2m}.
$$

<p>We seek, in the most general way, a differential equation of the form  
\( \frac{\partial \psi}{\partial t} = F(\psi) \), where \( F(\psi) \) involves \( \psi \) and/or its spatial derivatives, such that this plane wave is a solution.</p>

<p>For the wave written above, we have:</p>

$$
\frac{\partial \psi}{\partial t}
= -\,i\,\omega\,\psi
= -\,i\,\frac{\hbar k^{2}}{2m}\,\psi .
$$

<p>Therefore, \( F(\psi) = -\,i\,\frac{\hbar k^{2}}{2m}\,\psi \). But the Laplacian satisfies</p>

$$
\nabla^{2}\!\left(e^{\,i\vec k\cdot \vec r}\right) = -\,k^{2}\,e^{\,i\vec k\cdot \vec r},
\quad\Rightarrow\quad
\nabla^{2}\psi = -\,k^{2}\psi .
$$

<p>This suggests a simple form for \( F(\psi) \):</p>

$$
F(\psi)= i\,\frac{\hbar}{2m}\,\nabla^{2}\psi ,
$$

<p>which implies that de Broglie waves satisfy</p>

$$
\frac{\partial \psi}{\partial t}
= i\,\frac{\hbar}{2m}\,\nabla^{2}\psi .
$$

<p>Multiplying both sides by \( i\hbar \), we finally obtain:</p>

$$
i\hbar\,\frac{\partial \psi}{\partial t}
= -\,\frac{\hbar^{2}}{2m}\,\nabla^{2}\psi .
$$

<p>This is the famous Schrödinger equation! As we can see, it follows quite naturally from simple reasoning. Even if you don’t have the mathematical background to follow every step, you can still <em>feel</em> that there’s nothing particularly complicated about the math itself. So next time someone brings up quantum physics, be more impressed by the brilliant intuition of its founders than by the mathematical formalism — which, in truth, is far less intimidating than it looks.</p>
